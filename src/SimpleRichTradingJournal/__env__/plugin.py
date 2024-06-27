
def symbol_call(update_object: dict) -> None:
    # Is called when the cells of columns `Name`, `Symbol`, `ISIN`, `Type`, `Short`, `Sector` or `Category` are edited.
    # Receives the object `cellValueChanged` (see https://dash.plotly.com/dash-ag-grid/editing-and-callbacks).
    # The field "data" represents the <row record> (see below).
    # If something is changed, the update object must be edited in place, e.g.:
    #   >>> update_data["data"]["Symbol"] = your_api(update_data["data"]["Name"])
    return


def course_call(row_record: dict, manual_take_amount: bool) -> bool:
    # Is called if a record falls into the `Open Trade` category.
    # Receives the <row record> (see below) and `manual_take_amount` indicates whether the amount was entered manually.
    # The return value indicates whether something has been changed.
    # If something is changed, the <row record> must be edited in place, e.g.:
    #   >>> row_record["TakeCourse"] = your_api(row_record["Symbol"])
    # Furthermore, "TakeCourse" AND "TakeAmount" must be set:
    #   >>> row_record["TakeAmount"] = row_record["TakeCourse"] * row_record["n"]
    return False


def init_log(log_data: list[dict]) -> bool:
    # Is executed once during initialization.
    # Receives the data of the log memory, each field is a <row record> (see below).
    # The return value indicates whether this data should be directly
    # written to the disk.
    return False


def init_history(history_data: dict[int, dict]) -> bool:
    # Is executed once during initialization.
    # Receives the data of the history memory.
    # The return value indicates whether this data should be directly
    # written to the disk.
    # history_data: {history_id(int): {"time": seconds_since_epoch(int), "data": [<row record>, ...]}, ...}
    return False


# <row record> fields:
# (except for "id" and "cat", all fields can be unset or filled with `None`)
# {
#       id                 <int>
#       cat                <
#                           ''  : undefined
#                           'd' : deposit
#                           'p' : payout
#                           'i' : ITC (Interests, Taxes and other Costs or Income)
#                           'v' : dividend
#                           'tf': finalized trade
#                           'to': open trade
#                          >
#       mark               < 1 >
#       Name               <str>
#       Symbol             <str>
#       ISIN               <str>
#       Type               <str>
#       Category           <str>
#       Short              <bool>
#       Sector             <str>
#       Rating             <float>
#       n                  <float>
#       InvestTime         <time_str>
#       InvestAmount       <float>
#       InvestCourse       <float>
#       TakeTime           <time_str>
#       TakeAmount         <float>
#       TakeCourse         <float>
#       ITC                <float>  (Interests, Taxes and other Costs or Income)
#       Performance        <float>
#       Profit             <float>
#       Dividend           <float>
#       Note               <str>
#       HoldTime           <duration_str>
#       Performance/Day    <float>
#       Profit/Day         <float>
# }
