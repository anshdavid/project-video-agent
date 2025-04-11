# Video Agent

Video Agent is a tool designed to generate highly immersive and cinematic 5-second video ideas, scripts, and storyboards. It leverages advanced AI models to create detailed and hyper-realistic cinematography, making it ideal for creative professionals and enthusiasts looking to bring their video concepts to life.

## Setting
The project is structured as follows:
- **agent.py**: The main script that orchestrates the workflow of the agents.
- **models.py**: Contains the data models used for ideas, scripts, and storyboards.
- **prompts/**: Directory containing detailed prompts for the AI agents.
- **examples/**: Sample video files for reference.
- **state-history/**: Stores the state history of the agent's runs.
- **storyboard/**: Outputs the generated storyboards in JSON format.

## Prompts
The project uses three main prompts:
1. **Inception Prompt**: Generates creative and engaging video ideas.
2. **Writer Prompt**: Converts ideas into production-ready scripts.
3. **Director Prompt**: Transforms scripts into detailed storyboards.

Each prompt is designed to guide the AI agents in their respective tasks, ensuring high-quality outputs.

## How It Works
1. **User Input**: The user provides a prompt describing their video concept.
2. **Inception Agent**: Generates a list of creative video ideas based on the user input.
3. **Writer Agent**: Converts the ideas into detailed, production-ready scripts.
4. **Director Agent**: Creates a storyboard for the video, capturing the essence of the script in three dynamic moments.
5. **Output**: The final storyboard is saved as a JSON file in the `storyboard/` directory.

## How to Run
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set your OpenAI API key in the `key` file.
4. Run the main script using the command:
   ```
   python agent.py
   ```
5. Follow the prompts in the terminal to generate your video storyboard.

## Changing the Agents
To modify the agents used in the project, navigate to `agent.py` and locate the following lines:
```python
inception_agent = Agent("openai:gpt-4o", result_type=Inceptions, instrument=True, system_prompt=INCEPTION_PROMPT)
writer_agent = Agent("openai:o3-mini", result_type=Scripts, instrument=True, system_prompt=WRITER_PROMPT)
director_agent = Agent("openai:gpt-4o", result_type=DirectorEdit, instrument=True, system_prompt=PRODUCER_PROMPT)
```
You can replace the model names (e.g., `openai:gpt-4o`) with other supported models or adjust the system prompts as needed.

## Uploading the State Model
The state model is defined in `models.py` under the `POVGenState` class. You can extend or modify this class to include additional fields or functionality as required.

## Future Improvements
1. **Feedback Mechanism**: Implement a Pydantic node to gather user feedback on the generated ideas, scripts, and storyboards. This can be integrated into the workflow to refine outputs based on user preferences.
2. **Enhanced Prompts**: Add more detailed and diverse prompts to improve the quality and variety of generated content.
3. **Visualization**: Develop a graphical interface to visualize the generated storyboards and scripts interactively.
4. **Multi-Agent Collaboration**: Enable collaboration between multiple agents to handle complex video generation tasks.