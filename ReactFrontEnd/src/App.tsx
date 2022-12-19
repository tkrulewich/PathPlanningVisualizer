import React, { useEffect, useState } from 'react';

import logo from './logo.svg';
import './App.css';


// import bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';

import { Button, ButtonGroup, Container, Row, Col, Form } from 'react-bootstrap';




const App: React.FC = () => {
  const [gridWidth, setGridWidth] = useState(25);
  const [gridHeight, setGridHeight] = useState(25);
  const [numObstacles, setNumObstacles] = useState(10);
  const [obstacleList, setObstacleList] = useState([]); 

  const [Algorithm, setAlgorithm] = useState("Dijkstra");

  const [gridVideo, setGridVideo] = useState(null);
  const [gridImage, setGridImage] = useState(null);

  const [pathLength, setPathLength] = useState(0);
  const [pathTime, setPathTime] = useState(0);

  const [startNode, setStartNode] = useState([0, 0]);
  const [endNode, setEndNode] = useState([0, 0]);

  const [showPath, setShowPath] = useState(false);

  useEffect(() => {


  }, [gridVideo]);


  const getGridVideo = () => {
        // fetch the JSON Object with POST
        fetch('https://edwardkrulewich.com:8000/find_path', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            grid_width: gridWidth,
            grid_height: gridHeight,
            obstacles: obstacleList,
            algorithm: Algorithm,
            start: startNode,
            end: endNode
          })
        })
        .then(response => response.json())
        .then(data => {
          setGridVideo(data.video);
          setPathLength(data.path_length);
          setPathTime(data.path_time);
          setShowPath(true);
        
        }
      );
  }

  const getGridImage = () => {
      // fetch the JSON Object with POST
      fetch('https://edwardkrulewich.com:8000/make_grid', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          grid_width: gridWidth,
          grid_height: gridHeight,
          num_obstacles: numObstacles
        })
      })
      .then(response => response.json())
      .then(data => {

        setGridImage(data.image);
        setObstacleList(data.obstacles);
        setStartNode(data.start);
        setEndNode(data.end);
        setShowPath(false);
      }
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        {/* bootstrap two columns align to top*/}
        <Container>
          <Row className="align-items-start">
            <Col xs={4} className="align-self-start">
              <h1>Controls</h1>
              <Form>
                <Form.Group controlId="gridSizeControls">
                  <Form.Label>Grid Width: {gridWidth} </Form.Label>
                  <Form.Control type="range" min={25} max={75} onChange={(e) => setGridWidth(Number(e.target.value))} />

                  <Form.Label>Grid Height: {gridHeight} </Form.Label>
                  <Form.Control type="range" min={25} max={75} onChange={(e) => setGridHeight(Number(e.target.value))} />

                  <Form.Label>Number of Obstacles: {numObstacles} </Form.Label>
                  <Form.Control type="range" min={10} max={75} onChange={(e) => setNumObstacles(Number(e.target.value))} />

                  <Form.Label>Algorithm: </Form.Label>
                  <Form.Control as="select" onChange={(e) => setAlgorithm(e.target.value)}>
                    <option>Dijkstra</option>
                    <option>A*</option>
                    <option>RRT</option>
                  </Form.Control>
                </Form.Group>

              <Form.Group controlId="Path Planning Controls">
                <ButtonGroup>
                  <Button variant="primary" onClick={() => getGridImage()}>Generate Grid</Button>
                  <Button variant="primary" onClick={() => getGridVideo()}>Show Path</Button>
                </ButtonGroup>
              </Form.Group>

            </Form>
            <h1>Path Info</h1>
              <p>Path Length: {Math.round(pathLength * 100) / 100}</p>
              <p>Path Time: {Math.round(pathTime * 100) / 100}</p>
            </Col>
            <Col xs={8}>
        {showPath && gridVideo && <video src={"data:video/mp4;base64," + gridVideo} width={"100%"} height={"auto"} autoPlay={true} controls={false} loop={true} />}
        {!showPath && gridImage && <img src={"data:image/png;base64," + gridImage} width={"100%"} height={"auto"} />}
            </Col>
          </Row>
        </Container>
      </header>
    </div>
  );
}



export default App;
