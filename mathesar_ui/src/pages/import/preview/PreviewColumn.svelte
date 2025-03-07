<script lang="ts">
  import type { Column } from '@mathesar/api/rpc/columns';
  import { AbstractTypeControl } from '@mathesar/components/abstract-type-control';
  import NameWithIcon from '@mathesar/components/NameWithIcon.svelte';
  import type { AbstractType } from '@mathesar/stores/abstract-types/types';
  import { Checkbox, Dropdown, TextInput } from '@mathesar-component-library';

  export let isLoading = false;

  export let processedColumn: {
    column: Column;
    abstractType: AbstractType;
  };
  export let selected: boolean;
  export let displayName: string;
  export let updateTypeRelatedOptions: (options: Column) => Promise<unknown>;

  $: disabled = processedColumn.column.primary_key || isLoading;

  // TODO: Also validate with other column names
  function checkAndSetNameIfEmpty() {
    if (displayName.trim() === '') {
      displayName = processedColumn.column.name;
    }
  }
</script>

<div class="column">
  <div class="column-name">
    <Checkbox bind:checked={selected} {disabled} />
    <TextInput
      disabled={isLoading}
      bind:value={displayName}
      on:blur={checkAndSetNameIfEmpty}
    />
  </div>
  <Dropdown {disabled} triggerClass="column-type" triggerAppearance="plain">
    <NameWithIcon slot="trigger" icon={processedColumn.abstractType.getIcon()}>
      {processedColumn.abstractType.name}
    </NameWithIcon>
    <div slot="content" class="type-options-content" let:close>
      <AbstractTypeControl
        column={{
          ...processedColumn.column,
          abstractType: processedColumn.abstractType,
        }}
        showWarnings={false}
        on:cancel={close}
        save={async (opts) => {
          await updateTypeRelatedOptions({
            ...processedColumn.column,
            ...opts,
          });
          close();
        }}
      />
    </div>
  </Dropdown>
</div>

<style lang="scss">
  .column {
    flex-grow: 1;

    > :global(.column-type) {
      height: 2.2rem;
      width: 100%;
    }

    > .column-name {
      height: 3rem;
      padding: 0.35rem 0.6rem;
      display: flex;
      align-items: center;
      border-bottom: 1px solid var(--slate-200);

      :global(.checkbox) {
        flex-grow: 0;
        flex-shrink: 0;
        margin-right: 0.5rem;
      }
    }
  }

  .type-options-content {
    min-width: 18rem;
    max-width: 22rem;
    padding: var(--size-small);
  }
</style>
