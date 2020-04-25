#!/bin/sh
# automate release steps
#
#   --dry-run  - tell bumpversion to not make changes
# check local tests pass
if [ -e /usr/local/bin/gmake ]
then 
	MAKE=gmake
else
	MAKE=make
fi

if hg sum --remote
    then echo "** no remote changes **"
    else
    echo "** FAIL ** repository out of sync"
    exit 1
fi

# check setup.py required setup.py attributes
if python setup.py check -s
    then echo "** Attribute Testing passed. **"
    else
    echo "** FAIL ** Testing failed $?- Exiting release script"
    exit 1
fi

# check long_description RST formatting
if python setup.py check --restructuredtext -s
    then echo "** long_description RST Testing passed. **"
    else
    echo "** FAIL ** Testing failed $?- Exiting release script"
    exit 2
fi

# check unit tests
if py.test
    then echo "** Testing passed. **"
    else
    echo "** FAIL ** Testing failed $?- Exiting release script"
    exit 3
fi

# check docs build locally
cd docs
$MAKE clean
if $MAKE html
    then echo "** Doc Build passed. **"
    else
    cd ..
    echo "** FAIL ** Document Build failed - Exiting release script"
    exit 4
fi
cd ..
# check bumpversion
if bumpversion $1 --verbose --commit --tag patch
    then echo "** Version Bump passed. **"
    else
    echo "** FAIL ** Bumpversion failed - Exiting release script"
    exit 5
fi
# clean up the build directories
rm -rf dist/
rm -rf pysftp.egg-info/
# build
python setup.py sdist
