import { useCallback, useEffect, useState } from "react"
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
  Panel,
} from 'reactflow';
import { useSelector } from "react-redux";
import 'reactflow/dist/style.css';
import { Button, Card, CardBody, useDisclosure } from "@nextui-org/react";

import Editable from "../component/editable/main";
import NodePanel from "../component/nodePanel";
import { Link } from "react-router-dom";


const buildNodes = (nodes) => {
  console.log("Building nodes");
  console.log(nodes);
  const labelMapper = {
    "timer": (node) => {
      return `Timer ${node?.data?.time}s`;
    },
    "llm": (node) => {
      console.log(node);
      return `LLM ${node?.name}`;
    },
    "input": (node) => {
      return `Input ${node?.name}`;
    },
    "prompt": (node) => {
      return `Prompt ${node?.name}`;
    }

  }
  return nodes.map((node, index) => {
    return {
      id: node.id,
      position: { x: 200, y: 100 * (index + 1) },
      data: { label: labelMapper[node.type](node) }
    }
  });
}


const Agent = () => {
  const agent = useSelector((state) => state.agent);

  // const initialNodes = [
  //   { id: '1', position: { x: 0, y: 0 }, data: { label: '1' } },
  //   { id: '2', position: { x: 0, y: 100 }, data: { label: '2' } },
  // ];
  const initialEdges = [{ id: 'e1-2', source: '1', target: '2' }];

  const [openEditable, setOpenEditable] = useState(false);
  const [nodeType, setNodeType] = useState("");
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState(initialEdges);

  // TODO: Built nodes and edges with the agent data
  useEffect(() => {
    if (!agent.nodes) return;
    setNodes(buildNodes(agent.nodes));
    console.log(nodes);
  }, [agent?.nodes]);

  // Handlers
  // Actions on nodes
  // TODO: When selecting a node, open the editable panel
  const onNodesChange = useCallback((changes) => {
    console.log("Nodes changes");
    console.log(changes);
    setNodes((nodes) => applyNodeChanges(changes, nodes));
  }, [setEdges]);

  // Actions on edges
  const onEdgesChange = useCallback((changes) => {
    console.log("Edges changes");
    console.log(changes);
    setEdges((edges) => applyEdgeChanges(changes, edges));
  }, [setEdges]);

  // Actions on connecting nodes
  const onConnect = useCallback((params) => {
    console.log("Connect");
    console.log(params);
    setEdges((eds) => addEdge(params, eds));
  }, [setEdges]);

  return (
    <div className="flex flex-wrap w-screen h-screen flex-col gap-2 justify-center items-center">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      >
        <Panel position="top-left">
          <Button
            isIconOnly={true}
          >
            <Link to={`/project/${agent.project_id}`}>
              <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 12h14M5 12l4-4m-4 4 4 4" />
              </svg>
            </Link>
          </Button>
        </Panel>
        <Panel position="top-center">
          <Card shadow="sm">
            <CardBody>
              <h1>{agent.name}</h1>
            </CardBody>
          </Card>
        </Panel>
        <Panel position="bottom-center">
          <NodePanel setOpenEditable={setOpenEditable} setNodeType={setNodeType} />
        </Panel>
        <Editable isOpen={openEditable} type={nodeType} onOpenChange={setOpenEditable} />
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  )
}

export default Agent;
