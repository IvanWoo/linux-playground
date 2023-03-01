# ebpf

## python program probing

list python related USDT(User-level statically defined tracing)

```sh
bpftrace -l 'usdt:/usr/bin/python3:*'
```

```sh
usdt:/usr/bin/python3:python:audit
usdt:/usr/bin/python3:python:function__entry
usdt:/usr/bin/python3:python:function__return
usdt:/usr/bin/python3:python:gc__done
usdt:/usr/bin/python3:python:gc__start
usdt:/usr/bin/python3:python:import__find__load__done
usdt:/usr/bin/python3:python:import__find__load__start
usdt:/usr/bin/python3:python:line
```

### demo

```sh
python3 t.py
```

in another terminal

```sh
bpftrace -e 'usdt:/usr/bin/python3.10:function__entry {time("%H:%M:%S"); printf(" line filename=%s, funcname=%s, lineno=%d\n", str(arg0), str(arg1), arg2);}' -p $(ps aux | grep "python3 t.py" | awk '{ print $2 }' | head -n 1)
```

```sh
22:06:37 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:37 line filename=/usr/lib/python3.10/asyncio/futures.py, funcname=_set_result_unless_cancelled, lineno=309
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:37 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:37 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:37 line filename=/vagrant/ebpf/t.py, funcname=main, lineno=11
22:06:37 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=sleep, lineno=605
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=cancel, lineno=148
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_timer_handle_cancelled, lineno=1816
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=cancel, lineno=64
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=gather, lineno=684
22:06:37 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=_ensure_future, lineno=618
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_futures.py, funcname=isfuture, lineno=14
22:06:37 line filename=/usr/lib/python3.10/asyncio/coroutines.py, funcname=iscoroutine, lineno=177
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=create_task, lineno=431
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=add, lineno=86
22:06:37 line filename=/usr/lib/python3.10/asyncio/futures.py, funcname=_get_loop, lineno=297
22:06:37 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=_ensure_future, lineno=618
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_futures.py, funcname=isfuture, lineno=14
22:06:37 line filename=/usr/lib/python3.10/asyncio/coroutines.py, funcname=iscoroutine, lineno=177
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=create_task, lineno=431
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=add, lineno=86
22:06:37 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=__init__, lineno=663
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:37 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:37 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:37 line filename=/vagrant/ebpf/t.py, funcname=hello, lineno=4
22:06:37 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=sleep, lineno=593
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=create_future, lineno=427
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_later, lineno=702
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_at, lineno=724
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=103
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:37 line filename=/vagrant/ebpf/t.py, funcname=hello, lineno=4
22:06:37 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=sleep, lineno=593
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=create_future, lineno=427
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_later, lineno=702
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_at, lineno=724
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=103
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:37 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__lt__, lineno=120
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:37 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:37 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/futures.py, funcname=_set_result_unless_cancelled, lineno=309
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/futures.py, funcname=_set_result_unless_cancelled, lineno=309
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/vagrant/ebpf/t.py, funcname=hello, lineno=6
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=sleep, lineno=605
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=cancel, lineno=148
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_timer_handle_cancelled, lineno=1816
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=cancel, lineno=64
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/vagrant/ebpf/t.py, funcname=hello, lineno=6
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=sleep, lineno=605
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=cancel, lineno=148
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_timer_handle_cancelled, lineno=1816
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=cancel, lineno=64
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=_done_callback, lineno=720
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=_done_callback, lineno=720
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/vagrant/ebpf/t.py, funcname=main, lineno=12
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=_remove, lineno=39
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=_remove, lineno=39
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_until_complete_cb, lineno=184
22:06:38 line filename=/usr/lib/python3.10/asyncio/futures.py, funcname=_get_loop, lineno=297
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=stop, lineno=648
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_set_coroutine_origin_tracking, lineno=1899
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=_remove, lineno=39
22:06:38 line filename=/usr/lib/python3.10/asyncio/runners.py, funcname=_cancel_all_tasks, lineno=55
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=all_tasks, lineno=42
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=__len__, lineno=72
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=__iter__, lineno=63
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=__init__, lineno=17
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=__enter__, lineno=21
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=__exit__, lineno=27
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=_commit_removals, lineno=53
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=<setcomp>, lineno=61
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=run_until_complete, lineno=610
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_running, lineno=580
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_running, lineno=689
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_futures.py, funcname=isfuture, lineno=14
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=ensure_future, lineno=610
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=_ensure_future, lineno=618
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_futures.py, funcname=isfuture, lineno=14
22:06:38 line filename=/usr/lib/python3.10/asyncio/coroutines.py, funcname=iscoroutine, lineno=177
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=create_task, lineno=431
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=add, lineno=86
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=run_forever, lineno=587
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_running, lineno=580
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_running, lineno=689
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_set_coroutine_origin_tracking, lineno=1899
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=shutdown_asyncgens, lineno=535
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=__len__, lineno=72
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_until_complete_cb, lineno=184
22:06:38 line filename=/usr/lib/python3.10/asyncio/futures.py, funcname=_get_loop, lineno=297
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=stop, lineno=648
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_set_coroutine_origin_tracking, lineno=1899
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=_remove, lineno=39
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=run_until_complete, lineno=610
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_running, lineno=580
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_running, lineno=689
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_futures.py, funcname=isfuture, lineno=14
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=ensure_future, lineno=610
22:06:38 line filename=/usr/lib/python3.10/asyncio/tasks.py, funcname=_ensure_future, lineno=618
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_futures.py, funcname=isfuture, lineno=14
22:06:38 line filename=/usr/lib/python3.10/asyncio/coroutines.py, funcname=iscoroutine, lineno=177
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=create_task, lineno=431
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=add, lineno=86
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=run_forever, lineno=587
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_running, lineno=580
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_running, lineno=689
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_set_coroutine_origin_tracking, lineno=1899
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=shutdown_default_executor, lineno=560
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=call_soon, lineno=740
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_check_closed, lineno=513
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_call_soon, lineno=769
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=__init__, lineno=31
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_once, lineno=1821
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=select, lineno=452
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_process_events, lineno=592
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=time, lineno=693
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=_run, lineno=78
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_run_until_complete_cb, lineno=184
22:06:38 line filename=/usr/lib/python3.10/asyncio/futures.py, funcname=_get_loop, lineno=297
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=stop, lineno=648
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=_set_coroutine_origin_tracking, lineno=1899
22:06:38 line filename=/usr/lib/python3.10/_weakrefset.py, funcname=_remove, lineno=39
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=set_event_loop, lineno=775
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=get_event_loop_policy, lineno=736
22:06:38 line filename=/usr/lib/python3.10/asyncio/unix_events.py, funcname=set_event_loop, lineno=1430
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=set_event_loop, lineno=661
22:06:38 line filename=/usr/lib/python3.10/asyncio/unix_events.py, funcname=close, lineno=67
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=close, lineno=82
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_running, lineno=689
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_closed, lineno=679
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_close_self_pipe, lineno=93
22:06:38 line filename=/usr/lib/python3.10/asyncio/selector_events.py, funcname=_remove_reader, lineno=268
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_closed, lineno=679
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=get_key, lineno=181
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=get_map, lineno=273
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=__getitem__, lineno=70
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=_fileobj_lookup, lineno=216
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=_fileobj_to_fd, lineno=21
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=unregister, lineno=366
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=unregister, lineno=248
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=_fileobj_lookup, lineno=216
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=_fileobj_to_fd, lineno=21
22:06:38 line filename=/usr/lib/python3.10/asyncio/events.py, funcname=cancel, lineno=64
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=get_debug, lineno=1914
22:06:38 line filename=/usr/lib/python3.10/socket.py, funcname=close, lineno=498
22:06:38 line filename=/usr/lib/python3.10/socket.py, funcname=_real_close, lineno=494
22:06:38 line filename=/usr/lib/python3.10/socket.py, funcname=close, lineno=498
22:06:38 line filename=/usr/lib/python3.10/socket.py, funcname=_real_close, lineno=494
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=close, lineno=656
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_running, lineno=689
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=close, lineno=484
22:06:38 line filename=/usr/lib/python3.10/selectors.py, funcname=close, lineno=269
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=__del__, lineno=683
22:06:38 line filename=/usr/lib/python3.10/asyncio/base_events.py, funcname=is_closed, lineno=679
22:06:38 line filename=/usr/lib/python3.10/threading.py, funcname=_shutdown, lineno=1518
22:06:38 line filename=/usr/lib/python3.10/threading.py, funcname=ident, lineno=1145
22:06:38 line filename=/usr/lib/python3.10/threading.py, funcname=_stop, lineno=1028
22:06:38 line filename=/usr/lib/python3.10/threading.py, funcname=daemon, lineno=1183
22:06:38 line filename=/usr/lib/python3.10/threading.py, funcname=_maintain_shutdown_locks, lineno=800
22:06:38 line filename=/usr/lib/python3.10/threading.py, funcname=<listcomp>, lineno=810
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=shutdown, lineno=2167
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=acquire, lineno=912
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=flush, lineno=1077
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=acquire, lineno=912
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=stream, lineno=1237
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=stream, lineno=1237
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=stream, lineno=1237
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=release, lineno=919
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=close, lineno=988
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=_acquireLock, lineno=219
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=_releaseLock, lineno=228
22:06:38 line filename=/usr/lib/python3.10/logging/__init__.py, funcname=release, lineno=919
```

## ref

- [用 BPF 动态追踪 Python 程序](https://www.kawabangga.com/posts/4894)
