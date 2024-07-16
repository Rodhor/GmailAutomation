from config import create_link
from rich.console import Console

console = Console()


def get_labels(gmailservice):
    # retrieve labels through the googleAPI
    results = gmailservice.users().labels().list(userId="me").execute()
    labels = [label.get("name", "Unkown") for label in results.get("labels", [])]

    # if no labels were found, return None and inform the user
    if not labels:
        console.print("No labels found!")
        return None
    return labels


def get_from_headers(gmailservice):
    # initialize returnlist and retrieve all messagethreads through googleAPI
    from_header_values = []
    threads = (
        gmailservice.users().threads().list(userId="me").execute().get("threads", [])
    )
    # loop through the threads to extract the wanted data
    for thread in threads:
        tdata = (
            gmailservice.users().threads().get(userId="me", id=thread["id"]).execute()
        )
        for message in tdata["messages"]:
            # extract the needed information based on the dictionary keys
            headers = message["payload"]["headers"]
            from_header = [
                header["value"]
                for header in headers
                if header["name"].lower() == "from"
            ]
            from_header_values.extend(from_header)
            # clean up result upon returning
    return [
        header.split("<")[1].split(">")[0]
        for header in from_header_values
        if "<" in header and ">" in header
    ]


def move_email_to_label(gmailservice):
    pass


def create_labels(gmailservice):
    pass


def main():
    gmailservice = create_link()
    get_labels(gmailservice)
    senders = get_from_headers(gmailservice)

    console.print(senders)


if __name__ == "__main__":
    main()
