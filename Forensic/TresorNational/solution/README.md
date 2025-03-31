# Trésor National: Le fichier des Archives

## Write-up FR

Suivre les indices pour retrouver les différents artéfacts Linux. Pour les plus expérimentés un grep ou find pourrait permettre d'identifier le flag.
1. cat ~/readme.txt (indice sur history)
2. cat ~/.zsh_history > cat /history.txt (indice sur logs)
3. cat /var/log/log.txt (indice sur journaux serveurs webs)
4. cat /var/log/nginx/wwwlog.txt (indice sur cronjob)
5. cat /etc/cron.d/cron.txt > flag
 
## Write-up EN

Follow the clues to retrieve the different Linux artifacts. For the more experienced, a grep or find might help identify the flag.
1. cat ~/readme.txt (hint on history)
2. cat ~/.zsh_history > cat /history.txt (hint on logs)
3. cat /var/log/log.txt (hint on journaux serveurs webs)
4. cat /var/log/nginx/wwwlog.txt (hint on cronjob)
5. cat /etc/cron.d/cron.txt > flag

## Flag

`polycyber{y0u_foUn6_1hE_tra3sUr3}`
