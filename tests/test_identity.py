from ccos.kernel import CCOSKernel

def test_identity_adaptive_value_changes_without_core_mutation():
    kernel = CCOSKernel()
    core_before = dict(kernel.identity.state.core_values)
    kernel.remember("A neighbor helped me", impact_on_values={"cooperation": 0.5}, interpretation="help can build trust")
    assert kernel.identity.state.adaptive_values["cooperation"] > 0.7
    assert kernel.identity.state.core_values == core_before
    assert kernel.identity.state.revision == 1
