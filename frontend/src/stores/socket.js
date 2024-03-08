import { defineStore } from 'pinia';
import { io } from 'socket.io-client';
import { ref, watch } from 'vue';
import { Notify } from 'quasar';

const socket = io(window.location.href, {
  auth: {
    name: process.env.NAME,
    pwd: process.env.PASSWORD,
  },
  autoConnect: false,
});

export const useSocketStore = defineStore('SocketStore', () => {
  const curProgressNum = ref(0);
  const curProgressRatio = ref(0);
  const reqProgressNum = ref(null);
  let reqPayload = null;
  const curProgressObj = ref('');
  const failNum = ref(0);
  const isComplete = ref(false);

  function reqConnection(payload) {
    socket.connect();
    reqProgressNum.value = payload.length;
    reqPayload = payload;
  }

  function bindEvents() {
    socket.on('permission', ({ result }, cb) => {
      if (result === 'fail') {
        Notify.create('Connection refused');
        if (cb) cb();
      } else {
        socket.emit('send_mails', reqPayload);
      }
    });

    socket.on('send_mails', (result) => {
      const { uid, status } = result;

      curProgressObj.value = uid;
      curProgressNum.value++;
      if (status === 'fail') failNum.value++;
      curProgressRatio.value = (curProgressNum.value / reqProgressNum.value).toFixed(2);
    });

    socket.on('disconnect', () => {
      curProgressNum.value = 0;
      curProgressRatio.value = 0;
      reqProgressNum.value = null;
      curProgressObj.value = '';
      isComplete.value = true;
      failNum.value = 0;
    });
  }

  watch(curProgressNum, (v) => {
    if (v === reqProgressNum.value) {
      if (failNum.value) Notify.create(`Fail ${failNum.value} times. Check error.log for more details`);
      else {
        Notify.create({
          type: 'positive',
          icon: 'fa-solid fa-check',
          message: 'Success to send all mails to the users',
        });
      }
      socket.disconnect();
    }
  });

  return {
    curProgressNum,
    curProgressRatio,
    curProgressObj,
    isComplete,
    reqConnection,
    bindEvents,
  };
});
