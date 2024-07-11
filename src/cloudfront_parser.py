import urllib.parse
import re
from datetime import datetime
import user_agents

def parse_cloudfront_logs(log_file):

    # The first line is a version header, e.g.
    #
    #     b'#Version: 1.0\n'
    #
    next(log_file)

    # The second line tells us what the fields are, e.g.
    #
    #     b'#Fields: date time x-edge-location …\n'
    #
    header = next(log_file)

    field_names = [
        name.decode("utf8")
        for name in header.replace(b"#Fields:", b"").split()
    ]

    # For each of the remaining lines in the file, the values will be
    # space-separated, e.g.
    #
    #     b'2023-06-26  00:05:49  DUB2-C1  618  1.2.3.4  GET  …'
    #
    # Split the line into individual values, then combine with the field
    # names to generate a series of dict objects, one per log entry.
    #
    # For an explanation of individual fields, see the CloudFront docs:
    # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html#LogFileFormat
    numeric_fields = {
        "cs-bytes": int,
        "sc-bytes": int,
        "sc-content-len": int,
        "sc-status": int,
        "time-taken": float,
        "time-to-first-byte": float,
    }

    url_encoded_fields = {
        "cs-uri-stem",
        "cs-uri-query",
    }
    user_agent_field = "cs(User-Agent)"

    nullable_fields = {
        "cs(Cookie)",
        "cs(Referer)",
        "cs-uri-query",
        "fle-encrypted-fields",
        "fle-status",
        "sc-range-end",
        "sc-range-start",
        "sc-status",
        "ssl-cipher",
        "ssl-protocol",
        "x-forwarded-for",
    }
    bulk_logs = []

    # Create the new index with today's date stamp
    today = datetime.now().strftime('%Y-%m-%d')
    opensearch_index = f'cloudfront-{today}'


    for line in log_file:
        values = line.decode("utf8").strip().split("\t")
        keys_to_remove = []
        log_data = dict(zip(field_names, values))

        # Undo any URL-encoding in a couple of fields
        for name in url_encoded_fields:
            if name in log_data:
                log_data[name] = urllib.parse.unquote(log_data[name])

            user_agent = None  # Default definition
        if user_agent_field in log_data:
            user_agent = user_agents.parse(log_data[user_agent_field])

            # This is custom logic to parse the logs as per my requirements
            # Extract Puppet-related information
            if 'PuppetForge.gem' in log_data[user_agent_field]:
                puppet_info = re.split(r'%20|/', log_data[user_agent_field])
                if len(puppet_info) >= 6:
                    log_data.update({
                        "accessed_by": puppet_info[0],
                        "forge_gem_version": puppet_info[1],
                        "ruby_version": puppet_info[5],
                        "os": puppet_info[6],
                    })
            elif 'PMT' in log_data[user_agent_field]:
                #puppet_info = log_data[user_agent_field].split('%20')
                puppet_info = re.split(r'%20|/', log_data[user_agent_field])
                if len(puppet_info) >= 8:
                    log_data.update({
                        "accessed_by": puppet_info[4],
                        "puppet_version": puppet_info[5],
                        "ruby_version": puppet_info[7],
                        "os": puppet_info[8],
                    })
            else:
                log_data.update({
                    "accessed_by": "web"
                })

            log_data.update({
 
                "user_agent_family": user_agent.browser.family,
                "user_agent_version": user_agent.browser.version_string,
                "user_agent_os": user_agent.os.family,
                "user_agent_device": user_agent.device.family,
            })
 
        # Empty values in certain fields (e.g. ``sc-range-start``) are
        # represented by a dash; removing them.
        for name, value in log_data.items():
            if name in nullable_fields and value == "-":
                 keys_to_remove.append(name)

        for key in keys_to_remove:
            log_data.pop(key, None)   

            

        # Convert a couple of numeric fields into proper numeric types,
        # rather than strings.
        for name, converter_function in numeric_fields.items():
            try:
                if log_data[name] != '-':
                    log_data[name] = converter_function(log_data[name])
                else:
                    log_data[name] = None
            except ValueError:
                pass

        # Convert the date/time from strings to a proper datetime value.
        log_data["date"] = datetime.strptime(
            log_data.pop("date") + log_data.pop("time"),
            "%Y-%m-%d%H:%M:%S"
        )
        bulk_logs.append({"index": {"_index": opensearch_index}})
        bulk_logs.append(log_data)
    return bulk_logs
