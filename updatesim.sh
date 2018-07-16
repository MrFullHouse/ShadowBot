#!/bin/bash

cd /home/ubuntu/ShadowBot/simc_bfa/simc && git pull
cd /home/ubuntu/ShadowBot/simc_bfa/simc/engine/
make optimized
/bin/cp -f /home/ubuntu/ShadowBot/simc_bfa/simc/engine/simc /home/ubuntu/ShadowBot/output/
echo date " update complete!" >> /home/ubuntu/ShadowBot/update_simc.log
