// Libraries
import { useDispatch, useSelector } from "react-redux";
import { Input, ModalHeader, ModalBody, ModalFooter, Button } from "@nextui-org/react";
import { redirect } from "react-router-dom";

// Redux
import { createAgent } from "../../store/slice/agent";


const Agent = () => {
  const project = useSelector((state: any) => state.project);
  const dispatch = useDispatch();

  return (
    <>
      <ModalHeader>Add Agent</ModalHeader>
      <ModalBody>
        <Input
          id="agentName"
          type="text"
          label="Agent Name"
        ></Input>
        <Input
          id="agentDescription"
          type="text"
          label="Agent Description"
        ></Input>
      </ModalBody>
      <ModalFooter>
        <Button
          color="primary"
          onPress={() => {
            const agentInput = document.getElementById("agentName") as HTMLInputElement;
            const agentDescription = document.getElementById("agentDescription") as HTMLInputElement;
            dispatch(createAgent(
              {
                id: null,
                name: agentInput.value,
                description: agentDescription.value,
                project_id: project.id,
                nodes: [],
              }
            ));
          }}
        >Save</Button>
      </ModalFooter>
    </>
  )
}

export default Agent;
