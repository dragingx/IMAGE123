const { Client, Intents, MessageEmbed } = require('discord.js');
const axios = require('axios');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.MESSAGE_CONTENT] });

// Replace 'YOUR_BOT_TOKEN' with your actual Discord bot token
const token = 'MTQzNDAyOTAyMjUzNDMwNzkyMA.GZVbbY.yWBC4ANLj_DtG6zlBQ9IfEcOmNzmcXgXSzlxgI';

client.on('messageCreate', async message => {
    if (message.content === '/IPLOG') {
        await message.channel.send('Please send your Grabify link.');
        const filter = m => m.author.id === message.author.id;
        const collector = message.channel.createMessageCollector({ filter, max: 1, time: 60000 });

        collector.on('collect', async collected => {
            const grabifyLink = collected.content;
            try {
                const response = await axios.get(`https://api.grabify.link/v1/${grabifyLink.split('/').pop()}`);
                const ipInfo = response.data;
                const embed = new MessageEmbed()
                    .setTitle('IP Logger Results')
                    .setDescription(`IP Address: ${ipInfo.ip}\nLocation: ${ipInfo.country}, ${ipInfo.city}\nDevice: ${ipInfo.device}\nBrowser: ${ipInfo.browser}`);
                message.channel.send({ embeds: [embed] });
                message.channel.send('@everyone');
            } catch (error) {
                message.channel.send('Failed to retrieve IP information.');
            }
        });

        collector.on('end', collected => {
            if (collected.size === 0) {
                message.channel.send('No Grabify link provided. Command cancelled.');
            }
        });
    } else if (message.content.startsWith('/IMAGE')) {
        const args = message.content.split(' ');
        if (args.length < 2) {
            return message.channel.send('Please provide an image URL.');
        }
        const imageUrl = args[1];
        const embed = new MessageEmbed()
            .setImage(imageUrl);
        message.channel.send({ embeds: [embed] });
    }
});

client.login(token);
