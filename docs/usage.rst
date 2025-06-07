Usage
=====

Here are some examples to help you get started with kipu-python.

.. code-block:: python
   
    import asyncio
    from kipu import KipuClient

   # Example usage
    async def main():
        async with KipuClient(
            access_id="your_access_id",
            secret_key="your_secret_key",
            app_id="your_app_id"
        ) as client:
            # Get patient census as flattened DataFrame
            census_df = await client.get_patients_census({"phi_level": "high",
                                                            "page": 1, 
                                                            "per": 10})
            print(f"Found {len(census_df)} patients")

    asyncio.run(main())

Refer to the API Reference for detailed function descriptions.