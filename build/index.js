import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ErrorCode, ListToolsRequestSchema, McpError, } from "@modelcontextprotocol/sdk/types.js";
import * as fs from 'fs';
const server = new Server({
    name: "mcp-server-add",
    version: "1.0.0",
}, {
    capabilities: {
        tools: {}
    }
});
// Read visual novel data from JSON file
const vn_data_path = 'D:/workspace/vn_mcp/visual_novel_data.json';
const vn_list = JSON.parse(fs.readFileSync(vn_data_path, 'utf8'));
// Export the vn_list for use in other modules
export { vn_list };
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
            },
            {
                name: "search_visual_novels",
                description: "Search for visual novels by name or description",
                inputSchema: {
                    type: "object",
                    properties: {
                        query: { type: "string" }
                    },
                    required: ["query"]
                }
            },
            {
                name: "get_visual_novel_details",
                description: "Get detailed information about a specific visual novel by name",
                inputSchema: {
                    type: "object",
                    properties: {
                        name: { type: "string" }
                    },
                    required: ["name"]
                }
            },
            {
                name: "search_visual_novels_by_tags",
                description: "Find visual novels that contain specific tags",
                inputSchema: {
                    type: "object",
                    properties: {
                        tags: {
                            type: "array",
                            items: { type: "string" }
                        }
                    },
                    required: ["tags"]
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
    if (request.params.name === "search_visual_novels") {
        const args = request.params.arguments;
        const { query } = args;
        // Search for VNs that match the query in name or description
        const results = vn_list.filter((vn) => {
            const name = vn.name.toLowerCase();
            const desc = vn.vndesc[0].toLowerCase();
            const searchTerm = query.toLowerCase();
            return name.includes(searchTerm) || desc.includes(searchTerm);
        }).map((vn) => ({
            name: vn.name,
            url: vn.url
        }));
        return { toolResult: results };
    }
    if (request.params.name === "get_visual_novel_details") {
        const args = request.params.arguments;
        const { name } = args;
        // Find the visual novel by name (exact match)
        const vn = vn_list.find((v) => v.name.toLowerCase() === name.toLowerCase());
        if (!vn) {
            // If not found by exact match, try to find by partial match
            const partialMatch = vn_list.find((v) => v.name.toLowerCase().includes(name.toLowerCase()));
            if (partialMatch) {
                return { toolResult: partialMatch };
            }
            return { toolResult: { error: "Visual novel not found" } };
        }
        return { toolResult: vn };
    }
    if (request.params.name === "search_visual_novels_by_tags") {
        const args = request.params.arguments;
        const { tags } = args;
        if (!tags || tags.length === 0) {
            return { toolResult: { error: "No tags provided" } };
        }
        // Convert tags to lowercase for case-insensitive matching
        const searchTags = tags.map(tag => tag.toLowerCase());
        // Find VNs that have all the specified tags
        const results = vn_list.filter((vn) => {
            // Flatten the tags array and convert to lowercase
            const vnTags = vn.vntags[0].map((tag) => tag.toLowerCase());
            // Check if all search tags are present in the VN's tags
            return searchTags.every(searchTag => {
                return vnTags.some((vnTag) => vnTag.includes(searchTag));
            });
        }).map((vn) => ({
            name: vn.name,
            url: vn.url,
            matched_tags: searchTags
        }));
        return { toolResult: results };
    }
    throw new McpError(ErrorCode.InternalError, "Tool not found");
});
