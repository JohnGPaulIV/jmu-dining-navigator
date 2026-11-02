import requests


def download_image(image_id: str, file_name: str, output_file: str, full_path: bool) -> bool:
    """
    Download an image from Elevate DXP and save it to disk.

    image_id   : Elevate AEM image ID
    file_name  : file name requested from the service
    output_file: local output path or file name
    full_path  : if True, treat output_file as a full path; otherwise
                 write into GP/team25/webapp/images/
    """
    # Construct remote image URL
    url = f"https://images.elevate-dxp.com/adobe/assets/urn:aaid:aem:{image_id}/as/{file_name}"
    resp = requests.get(url)

    # Default local path (relative to project)
    path = f"GP/team25/webapp/images/{output_file}"

    if resp.status_code == 200:
        if (full_path):
            # Override with the full path if requested
            path = output_file

        # Save binary content to disk
        with open(path, "wb") as f:
            f.write(resp.content)
        return True

    # Return False on non-200 responses
    return False
