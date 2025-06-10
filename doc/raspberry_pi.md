# Установка на Raspberry Pi
1. Создайте файл службы:
    ```bash
    sudo nano /etc/systemd/system/weight_rs.service
    ```

2. Вставьте в файл следующий текст:

   ```ini
   [Unit]
   Description=Run Weight RS Reader at system startup
   After=network.target

   [Service]
   ExecStart=/project_path/venv/bin/python3 /project_path/src/main.py
   WorkingDirectory=/project_path
   StandardOutput=inherit
   StandardError=inherit
   Restart=always
   User=root

   [Install]
   WantedBy=multi-user.target
   ```

3. Замените путь к проекту. Сохраните файл и закройте редактор.

4. Активируйте и запустите службу:

   ```bash
   sudo systemctl enable weight_rs.service
   sudo systemctl start weight_rs.service
   ```

## Как контролировать работу скрипта?
После настройки службы вы можете контролировать её работу с помощью нескольких команд `systemd`:

1. **Просмотр статуса службы**:
   ```bash
   sudo systemctl status weight_rs.service
   ```

2. **Просмотр журнала службы**:
   ```bash
   sudo journalctl -u weight_rs.service
   ```

3. **Запуск и остановка службы вручную**:
   - Чтобы запустить службу вручную:
     ```bash
     sudo systemctl start weight_rs.service
     ```
   - Чтобы остановить службу:
     ```bash
     sudo systemctl stop weight_rs.service
     ```

4. **Перезагрузка службы**:
   Если вам нужно перезапустить службу после внесения изменений в скрипт или конфигурацию:
   ```bash
   sudo systemctl restart weight_rs.service
   ```

5. **Отключение службы**:
   Если вы хотите отключить автоматический запуск службы при старте системы:
   ```bash
   sudo systemctl disable weight_rs.service
   ```
