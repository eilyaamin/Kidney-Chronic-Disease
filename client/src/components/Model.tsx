import React from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Divider,
  Link,
  Image,
} from "@nextui-org/react";
import avatar from "../styles/assets/brain.png";

interface Props {
  name: string;
  description: string;
  accuracy: string;
}

const Model: React.FC<Props> = (props) => {
  return (
    <Card className="max-w-[400px]">
      <CardHeader className="flex gap-3">
        <Image
          alt="Machine Learning Model"
          height={40}
          width={40}
          radius="sm"
          src={avatar}
        />
        <div className="flex flex-col">
          <p className="text-md">{props.name}</p>
          <p className="text-small text-default-500">Accuracy: {props.accuracy}%</p>
        </div>
      </CardHeader>
      <Divider />
      <CardBody>
        <p>{props.description}</p>
      </CardBody>
      <Divider />
      <CardFooter>
        <Link
          isExternal
          showAnchorIcon
        >
          {props.name} examination form
        </Link>
      </CardFooter>
    </Card>
  );
};

export default Model;
