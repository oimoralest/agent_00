import { Input, ModalBody, ModalHeader, Select, Tabs, Tab } from "@nextui-org/react"
import { useState } from "react";
import { useSelector } from "react-redux";
import getAvailableTargets from "../../../utils/targets";

const InputNode = () => {
  const agent = useSelector((state: any) => state.agent);
  const [selectedTarget, setSelectedTarget] = useState(new Set([]));
  const [selectedOutputType, setSelectedOutputType] = useState(new Set([]));
  return (
    <>
      <ModalHeader>
        Input
      </ModalHeader>
      <ModalBody>
        <Input
          id="inputName"
          type="text"
          label="Input Name"
          isRequired={true}
        ></Input>
        <Input
          id="inputDescription"
          type="text"
          label="Description"
        ></Input>
        <Tabs aria-label="Input settings" disableAnimation={true}>
          <Tab key="output" title="Output" className="flex flex-col w-full gap-2">
            <Input
              id="outputName"
              type="text"
              label="Name"
            ></Input>
            <Select
              label="Type"
              placeholder="Select an output type"
              selectionMode="single"
              onSelect={(e) => console.log(e)}
              selectedKeys={selectedOutputType}
              onSelectionChange={setSelectedOutputType}
            >
            </Select>
          </Tab>
          <Tab key="target" title="Target" className="flex flex-col w-full gap-2">
            <Select
              label="Target"
              placeholder="Select a target"
              selectionMode="single"
              onSelect={(e) => console.log(e)}
              selectedKeys={selectedTarget}
              onSelectionChange={setSelectedTarget}
            >
              {getAvailableTargets(agent).map((target: any) => { console.log(target) })}
            </Select>
          </Tab>
        </Tabs>
      </ModalBody>
    </>
  )
}

export default InputNode;
