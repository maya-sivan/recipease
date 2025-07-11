import { Menu } from 'antd';
import { HomeTwoTone, EditTwoTone, CheckCircleTwoTone } from '@ant-design/icons';
import { Outlet, Link } from 'react-router-dom';
import { useState } from 'react';

const Layout: React.FC = () => {
  const [current, setCurrent] = useState('home');
  return (
    <>
      <Menu mode="horizontal" selectedKeys={[current]} onClick={(e) => setCurrent(e.key)}>
        <Menu.Item key="home" icon={<HomeTwoTone />}>
          <Link to="/">Home</Link>
        </Menu.Item>
        <Menu.Item key="register" icon={<EditTwoTone />} style={{ marginLeft: 'auto' }}>
          <Link to="/register">Register</Link>
        </Menu.Item>
        <Menu.Item key="login" icon={<CheckCircleTwoTone />}>
          <Link to="/login">Login</Link>
        </Menu.Item>
      </Menu>
      <Outlet />
    </>
  );
};

export default Layout;
