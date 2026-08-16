"""``rules.checks``: expression checks and issue codes."""
from ..session import safe_eval, selectors_match
from ..values import emit_issue


def validate_checks(session, report):
    for file in session.iter_files():
        ctx = session.context(file, rich=True)
        for bound in session.check_rules.for_file(ctx.get('suffix'), ctx.get('datatype')):
            if not selectors_match(None, ctx, compiled=bound.selector_asts):
                continue
            rule = bound.rule
            if checks_pass(rule.get('checks') or [], ctx):
                continue
            emit_issue(
                report,
                rule.get('issue') or {},
                file,
                'Schema check failed',
                default_code='CHECK_ERROR')


def checks_pass(checks, ctx):
    for expr in checks:
        if safe_eval(expr, ctx) is False:
            return False
    return True
