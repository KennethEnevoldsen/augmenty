import augmenty

def test_info():
    assert isinstance(augmenty.__version__, str)
    assert isinstance(augmenty.__url__, str)
    assert isinstance(augmenty.__title__, str)