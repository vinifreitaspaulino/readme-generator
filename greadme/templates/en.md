# Prompt — README.md Generator

## Context

You are a senior software engineer and technical writer with expertise in creating high-quality documentation for open-source projects. You will receive the project name, GitHub profile, repository name, primary language, a short description and the source code of its most relevant files (those exceeding 50 lines).

Your task is to thoroughly analyze the provided code, infer all necessary details not explicitly stated — such as the project's purpose, architecture, dependencies, data flow, entities, entry points, and any customization options — and produce a complete, professional `README.md` file suitable for the root of a GitHub repository.

Do not request clarification. Do not include any explanations or content outside the `README.md` document itself. If information cannot be reasonably inferred from the code, use a concise placeholder in brackets, such as `[insert demo link]`.

---

## Project Information

```
Project Name    : {project_name}
GitHub Profile  : {github_user}
Repository Name : {repository_name}
Primary Language: {type}
Short Description: {description}
```

### Source Files

These are the most relevant source code files:

````
[FILE CONTENTS HERE]
````

---

## Instructions

Using the project information and source files provided, generate a `README.md` file adhering to the structure and rules outlined below. Infer all content from the code where possible, ensuring the document is informative, accurate, and user-friendly.

### Rules

- Write exclusively in professional English, maintaining a concise and formal tone.
- Avoid emojis throughout the document.
- Ensure all Table of Contents links use proper Markdown anchors prefixed with `#`.
- All Mermaid diagrams must employ valid syntax compatible with GitHub's rendering engine.
- Badges must utilize the `flat-square` style from Shields.io, referencing the provided GitHub profile and repository name where applicable.
- When inferring customization options, command-line arguments, environment variables, or configuration files from the code, describe them clearly, including what each option does, default values (if any), and how to apply them.
- If no customization options are detected, omit the relevant subsection.

---

### Required Structure

**1. Title**  
The project name as an H1 heading, followed by an inferred one-line summary as a blockquote.

**2. Badges**  
Four inline `flat-square` badges: development status (e.g., active or archived, inferred if possible), license, last commit date, and primary language.

**3. Table of Contents**  
A numbered list with functional anchor links to every section and subsection below.

**4. Overview**  
Two to three paragraphs: First, describe the problem the project addresses and its target audience. Second, outline the core implementation logic inferred from the code. Third, if applicable, highlight any unique aspects such as performance optimizations or integrations. Include a `### Project Demonstration` subsection with a placeholder like `[insert screenshot or demo link]`.

**5. Key Features**  
4 to 6 bullet points inferred from the code, each starting with a bold label followed by a one-sentence description. Prioritize features that demonstrate value, such as core functionalities, integrations, or efficiencies.

**6. Technical Stack**  
A bulleted list inferred from imports, dependencies, file extensions, and structure:  
- Programming Language  
- Frameworks and Libraries  
- Data Persistence (e.g., databases, file systems)  
- Build and Deployment Tools  
- Any other relevant technologies

**7. Architecture**  
Three subsections:  

- `### Directory Structure` — A `text` code block displaying the inferred folder tree from provided file paths, with brief one-line annotations for key directories or files.  
- `### Data Flow` — A `mermaid` code block using `sequenceDiagram` with `autonumber` to illustrate the step-by-step flow of the primary use case inferred from the code.  
- `### System Components` — A brief description of major modules or components, their interactions, and any design patterns employed (e.g., MVC, modular).

**8. Getting Started**  
- `### Prerequisites` — List system requirements, software versions, and dependencies inferred from the code (e.g., Python version, required OS).  
- `### Installation` — Provide detailed, step-by-step instructions: Clone the repository, set up a virtual environment (if applicable, e.g., for Python), install dependencies using inferred commands (e.g., `pip install -r requirements.txt`), and any build steps like compilation or asset generation. Explain each step clearly for users of varying expertise.  
- `### Configuration` — If environment variables, config files, or setup parameters are detected in the code, list them with descriptions, examples, and how to set them (e.g., via `.env` file or command-line). Omit if none are present.

**9. Usage**  
A brief introductory paragraph explaining how to run the project, followed by a `bash` code block demonstrating the primary execution command(s) inferred from entry points or CLI definitions in the code. Include examples for common scenarios.

**10. Customization Options**  
If customization options (e.g., command-line flags, configuration parameters, or modular extensions) are inferred from the code, provide:  
- A bulleted or tabulated list of available options, including names, types (e.g., boolean, string), default values, and descriptions.  
- Examples of how to use them, such as modified run commands or config file snippets.  
- Explanation of how these options affect the project's behavior or output.  
Omit this section if no options are detected.

**11. Testing**  
Include only if test files, assertions, or a testing framework are detected in the source files. Describe the testing approach briefly, followed by a `bash` code block with the inferred command to run tests (e.g., `pytest`).

**12. Contribution Guidelines**  
A numbered list of steps: Fork the repository, create a feature branch, commit changes following [Conventional Commits](https://www.conventionalcommits.org/), push to the branch, and submit a pull request. Add notes on code style, testing requirements, and issue reporting.

**13. Author**  
```
**[Author Name]** (Infer from GitHub profile if possible, or use placeholder)  
- GitHub: [@{github_user}](https://github.com/{github_user})  
- LinkedIn: [profile](https://linkedin.com/in/profile) (Use placeholder if unknown)  
```

**14. License**  
A single sentence stating the license. Default to MIT if none is detected in the code or repository information.

---

## Expected Output

Output only the complete `README.md` file in Markdown format. Do not include any additional text, headers, or wrappers.