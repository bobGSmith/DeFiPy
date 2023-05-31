import asyncio

async def log_loop(event_filter, poll_interval, handle_event):
    '''where handle event is custom function for what to do with event (transaction)'''
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)
        
        
def filter_pending(w3, poll_interval, handle_event):
    '''filter for pending transactions'''
    tx_filter = w3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(tx_filter, poll_interval, handle_event)))
    finally:
        loop.close()