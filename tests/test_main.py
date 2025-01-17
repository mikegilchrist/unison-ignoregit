import pytest
from unittest import mock

from unison_ignoregit.main import main


@pytest.fixture
def cmd():
    return [
        "unison_ignoregit",
        "local_root",
        "ssh://remote_root",
        "-path",
        "path1",
        "-prefer",
        "root1",
    ]


@pytest.fixture
def mock_collect_ignoregits():
    def generator(abs_path):
        yield f"{abs_path}/stuff/data", f"{abs_path}/stuff/data/.ignoregit"

    with mock.patch("unison_ignoregit.main.collect_ignoregits_from_path") as m:
        m.side_effect = generator
        yield m


@pytest.fixture
def mock_run_cmd():
    with mock.patch("unison_ignoregit.main.run_cmd") as m:
        yield m


@pytest.fixture
def mock_files():
    # Python 3.6 `mock_open` doesn't seem to work properly
    def mock_iter():
        yield from mock_ignoregit_as_array

    with mock.patch(
        "builtins.open", mock.mock_open(read_data=mock_ignoregit_contents)
    ) as mock_file:
        mock_file.return_value.__iter__.side_effect = mock_iter
        yield mock_file


mock_ignoregit_as_array = [
    "*.py[co]",
]

mock_ignoregit_contents = "\n".join(mock_ignoregit_as_array)


@pytest.mark.usefixtures("mock_collect_ignoregits", "mock_files")
def test_calls_run_cmd(cmd, mock_run_cmd):
    main(cmd)
    mock_run_cmd.assert_called_once()


def test_no_args_calls_run_cmd(mock_run_cmd):
    main(["unison_ignoregit"])
    mock_run_cmd.assert_called_once()
    args = mock_run_cmd.call_args[0][0]
    assert args == ["unison"]


@pytest.mark.usefixtures("mock_collect_ignoregits", "mock_files")
def test_calls_run_cmd_with_regex_patterns(cmd, mock_run_cmd):
    main(cmd)
    args = mock_run_cmd.call_args[0][0]
    assert args[0] == "unison"
    assert args[1:7] == cmd[1:7]
    assert len(args) == len(cmd) + len(mock_ignoregit_as_array)

    for arg in args[7:]:
        assert arg.startswith("-ignore=")


@pytest.mark.usefixtures("mock_collect_ignoregits", "mock_files")
@pytest.mark.parametrize(
    "cmd",
    [
        # Local ambiguity
        ["unison_ignoregit", "local1", "local2", "-path", "path"],
        # Profile
        ["unison_ignoregit", "my_profile", "-path", "path"],
    ],
)
def test_does_not_add_patterns_when_unable_to(cmd, mock_run_cmd):
    main(cmd)
    mock_run_cmd.assert_called_once()
    args = mock_run_cmd.call_args[0][0]
    assert args[0] == "unison"
    assert len(args) == len(cmd)
    assert args[1:] == cmd[1:]


@pytest.mark.usefixtures("mock_collect_ignoregits", "mock_files")
def test_when_no_path_given_it_uses_local_root(mock_run_cmd):
    cmd = ["unison_ignoregit", "/home/john_doe", "ssh://remote/john_doe_data"]
    main(cmd)
    mock_run_cmd.assert_called_once()
    args = mock_run_cmd.call_args[0][0]
    assert args[0] == "unison"
    assert args[1:3] == cmd[1:3]
    assert len(args) == 4
    assert args[3] == r"-ignore=Regex ^stuff/data/(.+/)?[^/]*\.py[co](/.*)?$"


@pytest.mark.usefixtures("mock_files")
def test_ignoregit_in_root(cmd, mock_run_cmd):
    def generator(abs_path):
        yield f"{abs_path}", f"{abs_path}.ignoregit"

    with mock.patch("unison_ignoregit.main.collect_ignoregits_from_path") as m:
        m.side_effect = generator
        main(cmd)
    mock_run_cmd.assert_called_once()
    args = mock_run_cmd.call_args[0][0]
    assert args[0] == "unison"
    assert args[1:7] == cmd[1:7]
    assert len(args) == 8
    assert args[7] == r"-ignore=Regex ^path1/(.+/)?[^/]*\.py[co](/.*)?$"
