# Automating SQL Injection Analysis with LLM Agents: A GPT-4O and Llama-Index Framework

This project demonstrates an innovative approach to automating SQL injection analysis using advanced Large Language Models (LLMs). By integrating **GPT-4O** and **Llama-Index's ReAct Agent**, we developed a system capable of performing SQL injection tasks with minimal human intervention. Our framework bridges automation and intelligent decision-making, enabling precise, efficient, and scalable SQL injection operations.

## 🚀 Key Features

- **Automation of SQL Injection Tasks**: Implements scripts to perform SQL injection operations, such as retrieving table names, identifying user information, and extracting sensitive data.
- **ReAct Agent Integration**: Leverages the ReAct Agent framework from Llama-Index to guide the LLM in executing multi-step processes with contextual understanding.
- **LLM-Driven Logic**: Utilizes GPT-4O to parse prompts and dynamically generate queries tailored to specific injection scenarios.
- **Seamless Toolset**: Provides reusable tools for common SQL injection tasks (e.g., fetching table names, columns, and user data).
- **Highly Configurable**: Adjustable LLM parameters and retry mechanisms for optimized performance across diverse web applications.

## 📋 Application and Usage

This framework can be applied in security analysis, penetration testing, and educational environments where SQL injection concepts are explored. By automating key aspects of SQL injection operations, it significantly reduces manual efforts, allowing users to focus on higher-level analysis and strategy.
![Untitled drawing](https://github.com/user-attachments/assets/22c409fb-adee-42b0-822c-3349ff671cf4)

## 🌟 How It Works

1. **Tools for SQL Injection**: Scripts define specific tools to discover table names, extract columns, and fetch user data.
2. **LLM and Agent Integration**: GPT-4O processes the prompt, while the ReAct Agent coordinates the tools to execute the tasks step-by-step.
3. **Dynamic Querying**: The LLM generates and refines SQL queries based on the application's structure and the provided prompt.

## 📌 Example Use Case

With a simple prompt like:

```plaintext
Identify all the table names in the database. Determine which table contains user-related information, extract the details of all users, and retrieve the password associated with the user named 'Tom'.
```

The system autonomously interacts with the database, navigating through its schema to fetch and analyze the required data.

## 📷 Architecture Overview

(Add a visual representation of the architecture here to illustrate the interplay between LLM, ReAct Agent, and the SQL injection tools.)

## 💡 Why This Matters

This project showcases how cutting-edge AI techniques can augment traditional security practices. By combining automation with intelligent language models, this framework delivers unparalleled efficiency and accuracy in SQL injection analysis.
