<script lang="ts">
  import type { ComponentProps } from 'svelte';

  import { iconWarning } from '@mathesar-component-library';

  import MessageBox from './MessageBox.svelte';

  type $$Props = ComponentProps<MessageBox>;
</script>

<div class="warning-box">
  <MessageBox {...$$restProps} icon={iconWarning}><slot /></MessageBox>
</div>

<style>
  .warning-box {
    --MessageBox__background: var(--yellow-100);
    --MessageBox__border: solid 4px var(--yellow-300);
    --MessageBox__icon-color: var(--yellow-300);
  }
</style>
