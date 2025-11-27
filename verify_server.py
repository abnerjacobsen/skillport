import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure environment for the server
server_env = os.environ.copy()
server_env["SKILLPOD_SKILLS_DIR"] = os.path.abspath(".agent/skills")
server_env["SKILLPOD_EMBEDDING_PROVIDER"] = "none"
server_env["SKILLPOD_LOG_LEVEL"] = "ERROR"  # Reduce noise

# Define server parameters
server_params = StdioServerParameters(
    command="uv",
    args=["run", "skillpod"],
    env=server_env
)

async def run_test():
    print("Starting SkillPod MCP Client Verification...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize
            await session.initialize()
            print("✅ MCP Initialized")

            # 2. List Tools
            tools = await session.list_tools()
            tool_names = [t.name for t in tools.tools]
            print(f"✅ Found Tools: {tool_names}")
            
            # run_skill_command is disabled by default (Phase 5)
            expected_tools = ["search_skills", "load_skill", "read_skill_file"]
            missing = [t for t in expected_tools if t not in tool_names]
            if missing:
                print(f"❌ Missing tools! Expected at least {expected_tools}, missing {missing}")
                return

            # 3. Test search_skills
            print("\n--- Testing search_skills ---")
            search_result = await session.call_tool("search_skills", arguments={"query": "hello"})
            # fastmcp returns list of content blocks. 
            # The tool returns a dict, but via MCP protocol it comes wrapped in content.
            # Let's inspect the text content.
            print(f"Search Result: {search_result.content[0].text}")
            
            # 4. Test load_skill
            print("\n--- Testing load_skill ---")
            try:
                load_result = await session.call_tool("load_skill", arguments={"skill_name": "hello-world"})
                print(f"Load Result: {load_result.content[0].text[:50]}...") # Show first 50 chars
            except Exception as e:
                print(f"❌ load_skill failed: {e}")

            # 5. Test read_skill_file
            print("\n--- Testing read_skill_file ---")
            try:
                read_result = await session.call_tool("read_skill_file", arguments={"skill_name": "hello-world", "file_path": "hello.py"})
                print(f"Read Result: {read_result.content[0].text}")
            except Exception as e:
                print(f"❌ read_skill_file failed: {e}")

            # 6. Test run_skill_command - SKIPPED (disabled by default in Phase 5)
            # Agents should execute scripts directly using the path from load_skill
            print("\n--- Skipping run_skill_command (disabled by default) ---")

            print("\n✅ Verification Complete!")

if __name__ == "__main__":
    asyncio.run(run_test())
