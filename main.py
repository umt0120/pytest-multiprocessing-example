from concurrent.futures import ProcessPoolExecutor
from _pytest.capture import CaptureFixture


def print_message(num: int, message: str) -> None:
    print(f"{num} 番目のメッセージをprintします ... [{message}]")


def print_synchronously() -> None:
    for i in range(99):
        print_message(i, "print_synchronouslyから呼び出されました。")


def print_in_multi_process() -> None:
    with ProcessPoolExecutor(max_workers=None) as p:
        for i in range(99):
            p.submit(print_message, i, "print_in_multi_processから呼び出されました")


def test_print_synchronously(capfd: CaptureFixture) -> None:
    print_synchronously()

    out, err = capfd.readouterr()

    assert (
        str(out).split("\n")[0]
        == "0 番目のメッセージをprintします ... [print_synchronouslyから呼び出されました。]"
    )


def test_print_in_multi_process(capfd: CaptureFixture) -> None:
    print_in_multi_process()

    out, err = capfd.readouterr()
    out_list = sorted([line for line in str(out).split("\n") if line != ""])
    # マルチプロセスとcapfdを組み合わせると文字化けする
    assert out_list[0] == "0 番目のメッセージをprintします ... [print_in_multi_processから呼び出されました]"
