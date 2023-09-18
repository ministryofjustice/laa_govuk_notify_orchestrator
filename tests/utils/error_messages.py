class ErrorMessages:
    def __init__():
        pass

    def invalid_status_code(expected_code: int, observed_code: int) -> str:
        return f"Invalid status code. Expected: {expected_code}, "\
               f"got: {observed_code}"

    def invalid_url(expected_url: str, observed_url: str) -> str:
        return f"Invalid URL. Expected: {expected_url}, "\
               f"got: {observed_url}"
