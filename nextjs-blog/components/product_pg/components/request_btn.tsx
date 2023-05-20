import React from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Cross2Icon } from '@radix-ui/react-icons';
import st from '../../../styles/product_pg/request_btn.module.css';
import { useDispatch, useSelector } from 'react-redux';
import config from '../../../config';
import { RootState } from '../../../redux/reducers';
import styled from 'styled-components';
import { Alert } from 'antd';
import Spinner from '../../loader';

export default function Request_Btn(props) {
  let [msgState, statehandler] = React.useState('');
  let [loader, setLoader] = React.useState(false);

  const theme = {
    blue: {
      default: '#3f51b5',
      hover: '#283593',
    },
    pink: {
      default: '#e91e63',
      hover: '#ad1457',
    },
  };

  const Button = styled.button`
    background-color: ${(props) => theme[props.theme].default};
    color: white;
    padding: 5px 15px;
    border-radius: 5px;
    outline: 0;
    text-transform: uppercase;
    margin: 10px 0px;
    cursor: pointer;
    box-shadow: 0px 2px 2px lightgray;
    transition: ease background-color 250ms;
    &:hover {
      background-color: ${(props) => theme[props.theme].hover};
    }
    &:disabled {
      cursor: default;
      opacity: 0.7;
    }
  `;

  Button.defaultProps = {
    theme: 'blue',
  };

  const ButtonToggle = styled(Button)`
    opacity: 0.7;
    ${({ active }) =>
      active &&
      `
    opacity: 1; 
  `}
  `;

  function getCurrentDateTimeString() {
    const now = new Date();
    const year = now.getUTCFullYear();
    const month = now.getUTCMonth() + 1;
    const day = now.getUTCDate();
    const hours = now.getUTCHours();
    const minutes = now.getUTCMinutes();
    const seconds = now.getUTCSeconds();
    // const milliseconds = now.getUTCMilliseconds();

    // Zero-pad month, day, hours, minutes, and seconds to two digits
    const zeroPad = (num) => num.toString().padStart(2, '0');
    const monthStr = zeroPad(month);
    const dayStr = zeroPad(day);
    const hoursStr = zeroPad(hours);
    const minutesStr = zeroPad(minutes);
    const secondsStr = zeroPad(seconds);

    // Format the date-time string
    const dateTimeStr = `${year}-${monthStr}-${dayStr}   ${hoursStr}:${minutesStr}:${secondsStr}`;

    return dateTimeStr;
  }

  const request_body = {
    order_date_time: '2023-04-07   13:13:20',
    p_uid: props.p_uid,
    cus_uid: 'ff',
    message: 'string',
  };

  // {
  //   "id": "vycs78",
  //   "cus_uid": "vycs78",
  //   "order_date_time": "2023-04-23T14:07:45.946Z",
  //   "p_uid": "vycs78",
  //   "message": "string"
  // }

  function handleChange(event) {
    let msg = event.target.value;
    statehandler(msg);
  }

  const [visible, SetVisibility] = React.useState(0);

  let AlertComponent;

  if (visible == 0) {
    console.log('in state 0');
    <div></div>;
  } else if (visible == 1) {
    console.log('in state 1');
    AlertComponent = <Alert message="Please log in first" type="error" />;
  } else {
    console.log('in state 2');
    AlertComponent = (
      <Alert message="Order Succesfully placed" type="success" />
    );
  }

  // 0 if not visible, 1 if not looged in, 2 if logged in and successful .
  const { isLoggedIn } = useSelector((state: RootState) => state.storage);

  const queryid = useSelector((state: RootState) => state.storage.userID);
  const { apiUrl } = config;

  // AlertComponent = <Alert message="Bookmarked" type="warning" />

  // const jwt = useSelector((state) => state.storage.jwt);
  async function handleSubmit(event) {
    if (isLoggedIn) {
      request_body.order_date_time = getCurrentDateTimeString();
      request_body.message = msgState;
      request_body.cus_uid = queryid.toString();
      setLoader(true);
      const response = await fetch(
        `${apiUrl}/api/customers/${queryid}/orders`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // Authorization: `Bearer ${jwt}`,
          },
          body: JSON.stringify(request_body),
        }
      );
      setLoader(false);
      if (response.ok) {
        SetVisibility(2);
        console.log('response worked!');
        statehandler('');
      }
    } else {
      SetVisibility(1);
      // alert("Please log in first!");
    }
  }

  return (
    <div className={st.DialogRoot}>
      {AlertComponent}
      <Dialog.Root>
        <Dialog.Trigger asChild>
          <div className={st.button_wrapper}>
            <h3>Connect with the contractor</h3>
            {/* <button className={st.Button}>{props.btn_text}</button> */}
            <Button theme="pink">
              {loader ? <Spinner /> : props.btn_text}
            </Button>
          </div>
        </Dialog.Trigger>
        <Dialog.Portal>
          <Dialog.Overlay className={st.DialogOverlay} />
          <Dialog.Content className={st.DialogContent}>
            <Dialog.Title className={st.DialogTitle}>
              {props.modal_header}
            </Dialog.Title>
            <Dialog.Description className={st.DialogDescription}>
              {props.modal_description}
            </Dialog.Description>
            <fieldset className={st.Fieldset}>
              {/* <label className={st.Label} htmlFor="msg" >
              {props.label}
            </label> */}
              <input
                className={st.Input}
                id="name"
                defaultValue=""
                value={msgState}
                onChange={handleChange}
                placeholder="Enter Message..."
              />
            </fieldset>

            <div
              style={{
                display: 'flex',
                marginTop: 25,
                justifyContent: 'flex-end',
              }}
            >
              <Dialog.Close asChild>
                <Button theme="pink" onClick={handleSubmit}>
                  {loader ? <Spinner /> : props.modal_btn_text}
                </Button>
              </Dialog.Close>
            </div>
            <Dialog.Close asChild>
              <button className={st.IconButton} aria-label="Close">
                X
              </button>
            </Dialog.Close>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </div>
  );
}
