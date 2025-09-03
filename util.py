def parse_custom_input(s: str) -> list[int]:
    '''
    A utility function that receives a string of numbers separated by a comma and returns a list of those numbers'''
    try:
        return [int(x.strip()) for x in s.split(',') if x.strip()]
    except ValueError:
        return []
