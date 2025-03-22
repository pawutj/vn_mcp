import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ErrorCode, ListToolsRequestSchema, McpError, } from "@modelcontextprotocol/sdk/types.js";
const server = new Server({
    name: "mcp-server-add",
    version: "1.0.0",
}, {
    capabilities: {
        tools: {}
    }
});
const transport = new StdioServerTransport();
await server.connect(transport);
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [{
                name: "calculate_sum",
                description: "Add two numbers together",
                inputSchema: {
                    type: "object",
                    properties: {
                        a: { type: "number" },
                        b: { type: "number" }
                    },
                    required: ["a", "b"]
                }
            },
            {
                name: "get_random_password",
                description: "Get Random Password",
                inputSchema: {
                    type: "object",
                    properties: {},
                    required: []
                }
            },
            {
                name: "get_encode_extra_password",
                description: "Get Encode Extra Password",
                inputSchema: {
                    type: "object",
                    properties: {
                        a: { type: "string" },
                    },
                    required: ["a"]
                }
            }
        ]
    };
});
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    if (request.params.name === "get_random_password") {
        const args = request.params.arguments;
        return { toolResult: Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) };
    }
    if (request.params.name === "calculate_sum") {
        const args = request.params.arguments;
        const { a, b } = args;
        return { toolResult: a + b };
    }
    if (request.params.name === "get_encode_extra_password") {
        const args = request.params.arguments;
        const { a } = args;
        return { toolResult: a + "123" };
    }
    throw new McpError(ErrorCode.InternalError, "Tool not found");
});
