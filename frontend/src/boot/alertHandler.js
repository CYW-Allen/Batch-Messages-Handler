import { boot } from 'quasar/wrappers';
import { Notify } from 'quasar';

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async (/* { app, router, ... } */) => {
  Notify.setDefaults({
    type: 'negative',
    icon: 'fa-solid fa-trangle-exclamation',
    position: 'center',
    classes: 'text-h6 text-bold',
    actions: [{
      icon: 'fa-solid fa-xmark',
      color: 'white',
      round: true,
      class: 'q-pt-xs',
    }],
  });
});
