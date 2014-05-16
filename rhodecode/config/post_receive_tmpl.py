#!/usr/bin/env python
import os
import sys

try:
    import rhodecode
    RC_HOOK_VER = '_TMPL_'
    os.environ['RC_HOOK_VER'] = RC_HOOK_VER
    from rhodecode.lib.hooks import handle_git_post_receive as _handler
except ImportError:
    if os.environ.get('RC_DEBUG_GIT_HOOK'):
        import traceback
        print traceback.format_exc()
    rhodecode = None


def main():
    if rhodecode is None:
        # exit with success if we cannot import rhodecode !!
        # this allows simply push to this repo even without
        # rhodecode
        sys.exit(0)

    repo_path = os.path.abspath('.')
    push_data = sys.stdin.readlines()
    # os.environ is modified here by a subprocess call that
    # runs git and later git executes this hook.
    # Environ gets some additional info from rhodecode system
    # like IP or username from basic-auth
    _handler(repo_path, push_data, os.environ)
    sys.exit(0)

if __name__ == '__main__':
    main()