import { Drawer, Box, List, ListItemIcon, ListItem, ListItemButton, ListItemText, Divider, Badge } from "@mui/material";
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import PeopleIcon from '@mui/icons-material/People';
import CloudIcon from '@mui/icons-material/Cloud';
import CampaignIcon from '@mui/icons-material/Campaign';
import React from "react";
import { Links, NavLinks } from "../../constants";
import MenuButton from "../Button/MenuButton";
import { MenuButtonWrapper } from "../Wrapper/style";
import { BadgeSharp } from "@mui/icons-material";

const NavBar: React.FC = () => {

  const [open, setOpen] = React.useState(false);
  const [alerts, setAlerts] = React.useState<number>(1);

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpen(newOpen);
  };
  const iconSelector: React.ElementType = (text: string) => {
    switch (text) {
      case 'Management':
        return <ManageAccountsIcon />;
      case 'Devicelist':
        return <PeopleIcon />;
      case 'Weather':
        return <CloudIcon />;
      case 'Alert':
        return <Badge color="error" badgeContent={alerts}> < CampaignIcon color="error" /></Badge>;

      default:
        return <></>;
    }
  };

  const DrawerList = (
    <Box sx={{ width: 250, display: "block" }} role="presentation" onClick={toggleDrawer(false)} >
      <List>
        {NavLinks.map((text, index) => (
          <>
            <ListItem key={index} >
              <ListItemButton component="a" href={Links[index]} >
                <ListItemIcon>
                  {iconSelector(text)}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItemButton>
            </ListItem>
            <Divider component="li" />
          </>
        ))}
      </List>
    </Box>
  );

  return (
    <MenuButtonWrapper>
      <MenuButton onClick={toggleDrawer(true)} ></MenuButton>
      <Drawer open={open} onClose={toggleDrawer(false)}>{DrawerList}</Drawer>
    </MenuButtonWrapper>

  );
}


export default NavBar;
