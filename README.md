# EtherScan Scanner

Scans the [Foundation](https://foundation.app/) Ethereum address ([0xcda72070e455bb31c7690a170224ce43623d0b6f](https://etherscan.io/token/0x3B3ee1931Dc30C1957379FAc9aba94D1C48a5405?a=0xcda72070e455bb31c7690a170224ce43623d0b6f)) for incoming and outgoing transactions.

Generates a CSV output grouped by day.

**Incoming transactions:** NFTs being minted on the platform

**Outgoing transactions:** NFTs being sold on the platform

---

## Install

`git clone` this repo

## Setup

1. Open the repo: `cd scan_etherscan`
2. Get an API key from [Etherscan](https://etherscan.io/apis)
3. Create your `.env` file: `cp .env.example .env`
4. Open `.env` file and add your API key after `API_KEY=`

> You may need to install dotenv: `pip install python-dotenv`

## Run

`python fetch_json.py <output_file_name>`

> This will overwrite whatever is currently in `<output_file_name>`
