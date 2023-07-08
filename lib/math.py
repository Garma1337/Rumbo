# coding: utf-8

from typing import Any, List


class MathException(Exception):
    pass


class Math(object):

    @staticmethod
    def greedy_partition(objects: List[Any], partition_count: int, partition_size: int, value_key: str):
        for o in objects:
            if value_key not in o:
                raise ValueError(f'The value key "{value_key}" does not exist for every object')

        objects.sort(key=lambda o: o[value_key], reverse=True)

        if len(objects) % partition_count > 0:
            raise MathException(
                f'The number of objects ({len(objects)}) cannot be distributed equally to {partition_count} partitions.'
            )

        required_object_count: int = partition_count * partition_size
        if len(objects) < required_object_count:
            raise MathException(
                f'The number of objects ({len(objects)}) is smaller than the amount required ({required_object_count})'
            )

        partitions: List[List[Any]] = []
        for x in range(0, partition_count):
            partitions.append([])

        for o in objects:
            empty_partitions: List[List[Any]] = list(filter(lambda p: len(p) == 0, partitions))

            if len(empty_partitions) == 0:
                # Once every partition has at least one number in it
                # we push numbers into the partition with the lowest sum
                incomplete_partitions: List[List[Any]] = list(filter(lambda p: len(p) < partition_size, partitions))

                if len(incomplete_partitions) == 0:
                    continue

                lowest_sum_partition: List[Any] = incomplete_partitions[0]
                for incomplete_partition in incomplete_partitions:
                    if sum([p[value_key] for p in incomplete_partition]) < sum(
                            [p[value_key] for p in lowest_sum_partition]):
                        lowest_sum_partition = incomplete_partition

                partitions[partitions.index(lowest_sum_partition)].append(o)
            else:
                # As long as there are empty sets we are pushing numbers into them
                partitions[partitions.index(empty_partitions[0])].append(o)

        return partitions
