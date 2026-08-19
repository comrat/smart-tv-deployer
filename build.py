#!/usr/bin/env python

from utils.args import get_args, validate_args
from utils.deployer import SmartTVDeployer

def main():
    args = get_args()
    validate_args(args)
    deployer = SmartTVDeployer(args)
    deployer.run()

main()