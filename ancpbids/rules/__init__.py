def collect_rules():
    rules = []

    # use dynamic import to prevent circular dependencies when module is loaded
    import ancpbids.rules.rules_files as sr
    rules.append(sr.StaticStructureValidationRule)
    rules.append(sr.DatatypesValidationRule)
    rules.append(sr.EntitiesValidationRule)

    return rules
