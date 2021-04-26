def can_return_rows_from_bulk_insert(connection):
    return (
      getattr(
        connection.features,
        "can_return_ids_from_bulk_insert",
        getattr(
          connection.features,
          "can_return_rows_from_bulk_insert",
          False,
        ),
      )
    )
