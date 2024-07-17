from config import create_link
from rich.console import Console
from db import Database

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


def get_from_and_id_headers(gmailservice):
    # initialize returnlist and retrieve all messagethreads through googleAPI
    from_and_id_values = {}
    threads = (
        gmailservice.users().threads().list(userId="me").execute().get("threads", [])
    )
    # loop through the threads to extract the wanted data
    for thread in threads:
        tdata = (
            gmailservice.users().threads().get(userId="me", id=thread["id"]).execute()
        )
        for message in tdata["messages"]:
            # Extract headers
            headers = message["payload"]["headers"]
            from_email = None
            id_header = None

            for header in headers:
                if header["name"].lower() == "from":
                    if "<" in header["value"] and ">" in header["value"]:
                        from_email = header["value"].split("<")[1].split(">")[0]
                    else:
                        from_email = header["value"]
                elif header["name"].lower() == "message-id":
                    id_header = header["value"]

                if from_email and id_header:
                    from_and_id_values[id_header] = from_email
    return from_and_id_values


def move_email_to_label(gmailservice):
    pass


def create_labels(gmailservice):
    pass


def main():
    db = Database()
    gmailservice = create_link()
    labels = get_labels(gmailservice)
    email_information = get_from_and_id_headers(gmailservice)


if __name__ == "__main__":
    main()
