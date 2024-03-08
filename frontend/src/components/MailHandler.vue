<template>
  <q-card class="fit">
    <q-card-section v-if="!appStatus.isProcessing" class="fit row justify-center items-center">
      <q-field filled square class="col" bg-color="light-blue-1">
        <template v-slot:prepend>
          <div class="text-subtitle1 text-bold text-indigo">UID :</div>
        </template>
        <template v-slot:control>
          <div class="text-subtitle1">{{ cols[appStatus.field2ColIndex.uid] }}</div>
        </template>
      </q-field>

      <q-field filled square class="col" bg-color="light-blue-1">
        <template v-slot:prepend>
          <div class="text-subtitle1 text-bold text-indigo q-pl-sm" style="border-left: 2px solid lightblue;">
            Title :
          </div>
        </template>
        <template v-slot:control>
          <div class="text-subtitle1">{{ cols[appStatus.field2ColIndex.title] }}</div>
        </template>
      </q-field>

      <q-field filled square class="col" bg-color="light-blue-1">
        <template v-slot:prepend>
          <div class="text-subtitle1 text-bold text-indigo q-pl-sm" style="border-left: 2px solid lightblue;">
            Content :
          </div>
        </template>
        <template v-slot:control>
          <div class="text-subtitle1">{{ cols[appStatus.field2ColIndex.content] }}</div>
        </template>
      </q-field>

      <q-field filled square class="col" bg-color="light-blue-1">
        <template v-slot:prepend>
          <div class="text-subtitle1 text-bold text-indigo q-pl-sm" style="border-left: 2px solid lightblue;">
            PublicT :
          </div>
        </template>
        <template v-slot:control>
          <div class="text-subtitle1">{{ appStatus.publicTime }}</div>
        </template>
      </q-field>

      <q-btn icon="fa-regular fa-paper-plane" class="q-ml-sm" size="lg" color="green" push glossy @click="sendMails"
        :disable="appStatus.field2ColIndex.uid === null
          || appStatus.field2ColIndex.title === null
          || appStatus.field2ColIndex.content === null" />
    </q-card-section>

    <q-card-section v-else>
      <div class="text-h6 text-green-8 text-bold q-mb-md">
        <span class="q-mr-sm">Process mail sending</span>
        <q-spinner-dots color="green-8" />
      </div>
      <q-linear-progress size="30px" :value="socket.curProgressRatio" color="green-8" animation-speed="500">
        <div class="absolute-full flex flex-center">
          <q-badge color="white" text-color="green" :label="curProgressLabel" />
        </div>
      </q-linear-progress>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { computed, watch } from 'vue';
import dayjs from 'dayjs';
import { useAppStatusStore } from 'src/stores/appStatus';
import { useSocketStore } from 'src/stores/socket';

const appStatus = useAppStatusStore();
const socket = useSocketStore();
socket.bindEvents();

const cols = computed(() => Object.keys(appStatus.mails[0] || {}).filter((e) => e !== 'Index'));
const curProgressLabel = computed(() => `${parseInt(Number(socket.curProgressRatio) * 100, 10)}%`);

async function sendMails() {
  const { mails, field2ColIndex, publicTime } = appStatus;
  let mailPublicTime = publicTime;
  const estimatedFinishSending = dayjs().add(mails.length, 'seconds');
  const configedPublicTime = dayjs(publicTime).valueOf();

  appStatus.isProcessing = true;

  if (estimatedFinishSending.valueOf() > configedPublicTime) {
    mailPublicTime = estimatedFinishSending.format('YYYY/MM/DD HH:mm:ss');
    appStatus.publicTime = mailPublicTime;
  }
  mailPublicTime = dayjs(mailPublicTime).unix();

  socket.reqConnection(mails.map((mail) => ({
    title: mail[cols.value[field2ColIndex.title]],
    content: mail[cols.value[field2ColIndex.content]],
    author: 'adminstrator',
    publish_at: mailPublicTime,
    is_enable: true,
    scope_uid: [mail[cols.value[field2ColIndex.uid]]],
  })));
}

watch(() => socket.isComplete, (v) => {
  if (v) {
    appStatus.isProcessing = false;
    socket.isComplete = false;
  }
});
</script>

<style></style>
