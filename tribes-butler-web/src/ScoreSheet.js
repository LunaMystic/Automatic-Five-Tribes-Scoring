import React from 'react';
import { Card, Col, Row } from 'antd';
const ScoreSheet = ({merc_score_arr, ...rest}) => (
  <div className="site-card-wrapper">
    <Row gutter={16}>
      <Col span={8}>
        <Card title="Player One (Black)" bordered={false}>
          Score: {merc_score_arr[0]}
        </Card>
      </Col>
      <Col span={8}>
        <Card title="Player Two (Yellow)" bordered={false}>
            Score: {merc_score_arr[1]}
        </Card>
      </Col>
      <Col span={8}>
        <Card title="Player Three (Blue)" bordered={false}>
            Score: {merc_score_arr[2]}
        </Card>
      </Col>
    </Row>
  </div>
);
export default ScoreSheet;