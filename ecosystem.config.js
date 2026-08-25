module.exports = {
  apps: [
    {
      name: "discord-cog-bot",
      script: "src/bot.py",
      interpreter: "python", // Uses system Python or specify ".venv/bin/python" / ".venv/Scripts/python.exe"
      autorestart: true,
      watch: false, // Set to true or ['src/cogs'] if you want PM2 to auto-restart on file changes
      max_memory_restart: "500M",
      env: {
        PYTHONUNBUFFERED: "1",
        NODE_ENV: "production",
      },
    },
  ],
};
