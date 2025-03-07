<script lang="ts">
  import { _ } from 'svelte-i18n';

  import AppSecondaryHeader from '@mathesar/components/AppSecondaryHeader.svelte';
  import { iconEdit, iconPermissions, iconSchema } from '@mathesar/icons';
  import LayoutWithHeader from '@mathesar/layouts/LayoutWithHeader.svelte';
  import type { Database } from '@mathesar/models/Database';
  import type { Schema } from '@mathesar/models/Schema';
  import { makeSimplePageTitle } from '@mathesar/pages/pageTitleUtils';
  import {
    getSchemaPageExplorationsSectionUrl,
    getSchemaPageTablesSectionUrl,
    getSchemaPageUrl,
  } from '@mathesar/routes/urls';
  import { modal } from '@mathesar/stores/modal';
  import { queries } from '@mathesar/stores/queries';
  import { currentTablesData as tablesStore } from '@mathesar/stores/tables';
  import AddEditSchemaModal from '@mathesar/systems/schemas/AddEditSchemaModal.svelte';
  import { logEvent } from '@mathesar/utils/telemetry';
  import { Button, Icon, TabContainer } from '@mathesar-component-library';

  import AddTableModal from './AddTableModal.svelte';
  import ExplorationSkeleton from './ExplorationSkeleton.svelte';
  import SchemaExplorations from './SchemaExplorations.svelte';
  import SchemaOverview from './SchemaOverview.svelte';
  import SchemaPermissionsModal from './SchemaPermissionsModal.svelte';
  import SchemaTables from './SchemaTables.svelte';
  import TableSkeleton from './TableSkeleton.svelte';

  export let database: Database;
  export let schema: Schema;
  export let section: string;

  const editSchemaModal = modal.spawnModalController();
  const addTableModal = modal.spawnModalController();
  const permissionsModal = modal.spawnModalController();

  // NOTE: This has to be same as the name key in the paths prop of Route component
  type TabsKey = 'overview' | 'tables' | 'explorations';
  type TabItem = {
    label: string;
    id: TabsKey;
    count?: number;
    href: string;
  };

  $: tablesMap = $tablesStore.tablesMap;
  $: explorationsMap = $queries.data;
  $: tablesRequestStatus = $tablesStore.requestStatus;
  $: explorationsRequestStatus = $queries.requestStatus;

  $: tabs = [
    {
      label: $_('overview'),
      id: 'overview',
      href: getSchemaPageUrl(database.id, schema.oid),
    },
    {
      label: $_('tables'),
      id: 'tables',
      showCount: tablesRequestStatus.state === 'success',
      count: tablesMap.size,
      href: getSchemaPageTablesSectionUrl(database.id, schema.oid),
    },
    {
      label: $_('explorations'),
      id: 'explorations',
      showCount: explorationsRequestStatus.state === 'success',
      count: explorationsMap.size,
      href: getSchemaPageExplorationsSectionUrl(database.id, schema.oid),
    },
  ] as TabItem[];

  $: activeTab = tabs.find((tab) => tab.id === section) || tabs[0];

  function handleEditSchema() {
    editSchemaModal.open();
  }

  $: ({ name, description, tableCount, currentAccess } = schema);
  $: ({ currentRoleOwns } = currentAccess);

  logEvent('opened_schema', {
    database_name: database.name,
    schema_name: $name,
    source: 'schema_page',
  });
</script>

<svelte:head><title>{makeSimplePageTitle($name)}</title></svelte:head>

<LayoutWithHeader
  restrictWidth
  cssVariables={{
    '--max-layout-width': 'var(--max-layout-width-console-pages)',
    '--layout-background-color': 'var(--sand-50)',
  }}
>
  <AppSecondaryHeader
    slot="secondary-header"
    pageTitleAndMetaProps={{
      name: $name,
      icon: iconSchema,
    }}
  >
    <div slot="action">
      <Button
        on:click={handleEditSchema}
        appearance="secondary"
        disabled={!$currentRoleOwns}
      >
        <Icon {...iconEdit} />
        <span>{$_('edit_schema')}</span>
      </Button>
      <Button appearance="secondary" on:click={() => permissionsModal.open()}>
        <Icon {...iconPermissions} />
        <span>{$_('schema_permissions')}</span>
      </Button>
    </div>

    <svelte:fragment slot="bottom">
      {#if $description}
        <span class="description">
          {$description}
        </span>
      {/if}
    </svelte:fragment>
  </AppSecondaryHeader>

  <TabContainer {activeTab} {tabs} uniformTabWidth={false}>
    <div slot="tab" let:tab class="tab-header-container">
      <span>{tab.label}</span>
      {#if tab.count !== undefined && tab.showCount}
        <span class="count">{tab.count}</span>
      {/if}
    </div>
    {#if activeTab?.id === 'overview'}
      <div class="tab-container">
        <SchemaOverview
          {tablesRequestStatus}
          {tablesMap}
          {explorationsMap}
          {database}
          {schema}
          {explorationsRequestStatus}
          onCreateEmptyTable={() => addTableModal.open()}
        />
      </div>
    {:else if activeTab?.id === 'tables'}
      <div class="tab-container">
        {#if tablesRequestStatus.state === 'processing'}
          <TableSkeleton numTables={$tableCount} />
        {:else}
          <SchemaTables
            {tablesMap}
            {database}
            {schema}
            onCreateEmptyTable={() => addTableModal.open()}
          />
        {/if}
      </div>
    {:else if activeTab?.id === 'explorations'}
      <div class="tab-container">
        {#if explorationsRequestStatus.state === 'processing'}
          <ExplorationSkeleton />
        {:else}
          <SchemaExplorations
            hasTablesToExplore={!!tablesMap.size}
            {explorationsMap}
            {database}
            {schema}
          />
        {/if}
      </div>
    {/if}
  </TabContainer>
</LayoutWithHeader>

<AddEditSchemaModal controller={editSchemaModal} {database} {schema} />
<AddTableModal controller={addTableModal} {schema} {tablesMap} />
<SchemaPermissionsModal controller={permissionsModal} {schema} />

<style lang="scss">
  .tab-container {
    padding: var(--size-xx-large) 0;
  }

  .tab-header-container {
    display: flex;
    align-items: center;

    > :global(* + *) {
      margin-left: 0.25rem;
    }

    .count {
      border-radius: var(--border-radius-l);
      background: var(--slate-200);
      font-size: var(--text-size-small);
      text-align: center;
      padding: 0.071rem 0.5rem;
      margin-left: 0.5rem;
    }
  }
</style>
