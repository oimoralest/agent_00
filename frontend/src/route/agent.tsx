import { useCallback, useEffect, useState } from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  Panel,
} from "reactflow";
import { useSelector } from "react-redux";
import "reactflow/dist/style.css";
import { Button, Card, CardBody } from "@nextui-org/react";
import { Link } from "react-router-dom";

import Editable from "../component/editable/main";
import NodePanel from "../component/nodePanel";

const CustomEdge = ({ id, sourceX, sourceY, targetX, targetY, markerEnd }) => {
  const edgePath = `M${sourceX},${sourceY} L${targetX},${targetY}`;
  return (
    <g>
      <path
        id={id}
        style={{
          stroke: "#000",
          strokeWidth: 2,
          strokeDasharray: "5,5",
          animation: "dash 1.5s linear infinite",
        }}
        d={edgePath}
        markerEnd={markerEnd}
      />
      <style>
        {`
          @keyframes dash {
            to {
              stroke-dashoffset: -20;
            }
          }
        `}
      </style>
    </g>
  );
};

// Build Nodes
const buildNodes = (nodes) => {
  const labelMapper = {
    timer: (node) => {
      return `Timer ${node?.data?.time}s`;
    },
    llm: (node) => {
      console.log(node);
      return `LLM ${node?.name}`;
    },
    input: (node) => {
      return `Input ${node?.name}`;
    },
    prompt: (node) => {
      return `Prompt ${node?.name}`;
    },
  };
  return nodes?.map((node, index) => ({
    id: node.id,
    position: node.position || { x: 200 * (index + 1), y: 100 * (index + 1) },
    data: { label: node.name || node.type },
    style: { border: "1px solid #777", padding: "10px", borderRadius: "8px" }, // Node style
  }));
};

const Agent = () => {
  const agent = useSelector((state) => state.agent);

  const [openEditable, setOpenEditable] = useState(false);
  const [nodeType, setNodeType] = useState("");
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    setNodes(buildNodes(nodes));
    setEdges(edges);
  }, []);

  // Handlers
  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  return (
    <div className="flex flex-wrap w-screen h-screen flex-col gap-2 justify-center items-center">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        edgeTypes={{ default: CustomEdge }} // Usar el CustomEdge
      >
        <Panel position="top-left">
          <Button isIconOnly={true}>
            <Link to={`/project/${agent?.project_id}`}>
              <svg
                className="w-6 h-6 text-gray-800 dark:text-white"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M5 12h14M5 12l4-4m-4 4 4 4"
                />
              </svg>
            </Link>
          </Button>
        </Panel>
        <Panel position="top-center">
          <Card shadow="sm">
            <CardBody>
              <h1>{agent?.name || ""}</h1>
            </CardBody>
          </Card>
        </Panel>
        <Panel position="bottom-center">
          <NodePanel
            setOpenEditable={setOpenEditable}
            setNodeType={setNodeType}
          />
        </Panel>
        <Editable
          isOpen={openEditable}
          type={nodeType}
          onOpenChange={setOpenEditable}
        />
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
};

export default Agent;
