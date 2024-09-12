// Libraries
import { useSelector } from "react-redux";
import { Button, Card, CardBody, Tooltip, useDisclosure } from "@nextui-org/react";
import { Link } from "react-router-dom";


import Editable from "../component/editable/main";


const Project = () => {
  const { agents } = useSelector((state) => state.project);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  const renderAgents = () => {
    return (
      agents.map((agent) => {
        console.log(agent);
        return (
          <Card
            key={agent.id}
            className="w-2/4 h-16 text-center" shadow="sm"
            isPressable={true}
            isHoverable={true}
          >
            <CardBody className="w-full h-full m-0 p-0">
              <Link to={`/agent/${agent.id}`}
                className="w-full h-full text-center m-auto flex justify-center items-center"
              >
                {agent.name}
              </Link>
            </CardBody>
          </Card>
        )
      })
    )
  }

  return (
    <div>
      <div className="flex flex-wrap w-screen h-screen flex-col gap-2 justify-center items-center"
        style={{
          userSelect: "none",
          msUserSelect: "none",
          MozUserInput: "none",
          WebkitUserSelect: "none",
          KhtmlUserSelect: "none",
          WebkitTouchCallout: "none",
        }}
      >
        {renderAgents()}
        <Tooltip
          showArrow={true}
          content="Add Agent"
          placement="bottom"
        >
          <Button
            isIconOnly={true}
            onPress={onOpen}
          >
            <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
              <path fillRule="evenodd" d="M2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10S2 17.523 2 12Zm11-4.243a1 1 0 1 0-2 0V11H7.757a1 1 0 1 0 0 2H11v3.243a1 1 0 1 0 2 0V13h3.243a1 1 0 1 0 0-2H13V7.757Z" clipRule="evenodd" />
            </svg>
          </Button>
        </Tooltip>
        <Editable isOpen={isOpen} onOpenChange={onOpenChange} type={'agent'} />
      </div>
    </div>
  );
};

export default Project;
