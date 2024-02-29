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
      <div class="text-h6 text-green-8 text-bold q-mb-md">{{ `The mail for ${curProgressUID} is processing...` }}</div>
      <q-linear-progress size="30px" :value="curProgress" color="green-8">
        <div class="absolute-full flex flex-center">
          <q-badge color="white" text-color="green" :label="curProgressLabel" />
        </div>
      </q-linear-progress>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useQuasar } from 'quasar';
import dayjs from 'dayjs';
import axios from 'axios';
import { useAppStatusStore } from 'src/stores/appStatus';

const $q = useQuasar();
const appStatus = useAppStatusStore();

const cols = computed(() => Object.keys(appStatus.mails[0] || {}).filter((e) => e !== 'Index'));
const curProgress = ref(0);
const curProgressLabel = computed(() => `${parseInt(Number(curProgress.value) * 100, 10)}%`);
const curProgressUID = ref('');

async function sendMails() {
  appStatus.isProcessing = true;
  try {
    const { mails, field2ColIndex, publicTime } = appStatus;
    let mailPublicTime = publicTime;
    const estimatedFinishSending = dayjs().add(mails.length, 'seconds');
    const configedPublicTime = dayjs(publicTime).valueOf();

    if (estimatedFinishSending.valueOf() > configedPublicTime) {
      mailPublicTime = estimatedFinishSending.format('YYYY/MM/DD HH:mm:ss');
      appStatus.publicTime = mailPublicTime;
    }
    mailPublicTime = dayjs(mailPublicTime).unix();

    for (let i = 0; i < mails.length; i++) {
      const mailInfo = {
        title: mails[i][cols.value[field2ColIndex.title]],
        content: mails[i][cols.value[field2ColIndex.content]],
        author: 'adminstrator',
        publish_at: mailPublicTime,
        is_enable: true,
        scope_uid: [mails[i][cols.value[field2ColIndex.uid]]],
      };

      curProgressUID.value = mails[i][cols.value[field2ColIndex.uid]];
      curProgress.value = ((i + 1) / mails.length).toFixed(2);

      // eslint-disable-next-line no-await-in-loop
      const result = (await axios.post(`${appStatus.svrUrl}/msg`, mailInfo)).data;
      if (result === 'fail') throw new Error(`Fail to send mail to uid ${curProgressUID.value}`);
    }

    $q.notify({
      type: 'positive',
      icon: 'fa-solid fa-check',
      message: 'Success to send all mails to the users',
    });
  } catch (err) {
    console.log('[sendMails] Error:', err);
    $q.notify({ message: 'Fail to send mails. Check error.log for more details' });
  }

  appStatus.isProcessing = false;
  curProgress.value = 0;
  curProgressUID.value = '';
}
</script>

<style></style>
