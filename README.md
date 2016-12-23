# Clouden Xmas
Kenneth Falck <<kennu@clouden.net>> 2016

This is the source code project for https://xmas.clouden.net. It's probably mostly interesting just to look at.

You probably need to tweak stack/site.yml and stack/api.yml if you want to actually use
the code.

Subfolder descriptions:

* <a href="service">service</a> - Serverless project, forwards REST API requests to AWS IoT
* <a href="stack">stack</a> - Separate CloudFormation stacks for persistent resources and API Gateway custom domain setup
* <a href="thing">thing</a> - Code for MIDI and GPIO integration on Raspberry Pi, listens to AWS IoT events
* <a href="ui">ui</a> - The HTML web UI
