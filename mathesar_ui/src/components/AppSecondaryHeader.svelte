<script lang="ts">
  import type { ComponentProps } from 'svelte';

  import PageTitleAndMeta from './PageTitleAndMeta.svelte';

  export let pageTitleAndMetaProps: ComponentProps<PageTitleAndMeta>;
  export let restrictWidth = true;
</script>

<div class="container">
  <div class="content" class:restrict-width={restrictWidth}>
    <div class="page-title-and-meta-container">
      <PageTitleAndMeta {...pageTitleAndMetaProps}>
        <slot slot="action" name="action" />
        <slot slot="bottom" name="bottom" />
      </PageTitleAndMeta>
    </div>
  </div>
</div>

<style>
  .container {
    background-color: var(--sand-200);
  }
  .content {
    padding: var(
      --AppSecondaryHeader__padding,
      var(--size-x-large) var(--page-padding-x)
    );
  }
  .content.restrict-width {
    max-width: var(--max-layout-width);
    margin-left: auto;
    margin-right: auto;
  }
</style>
